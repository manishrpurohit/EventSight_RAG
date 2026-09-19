import os
import pandas as pd
from typing import Dict, Any, Tuple
from langchain_groq import ChatGroq

from src.config import GROQ_MODEL_NAME, get_groq_api_key
from src.database import DATABASE_SCHEMA, init_database, execute_sql
from src.vectorstore import retrieve_documents, create_context, format_sources

def get_llm(api_key: str = None) -> ChatGroq:
    """Instantiate and return ChatGroq model instance."""
    key = api_key or get_groq_api_key()
    if not key:
        raise ValueError("Groq API Key is missing. Please set GROQ_API_KEY environment variable or enter it in the app settings.")
    return ChatGroq(
        model=GROQ_MODEL_NAME,
        temperature=0,
        api_key=key
    )

def classify_question(question: str, api_key: str = None) -> str:
    """
    Classify incoming natural language question into SQL, RAG, or BOTH.
    """
    llm = get_llm(api_key)
    prompt = f"""
You are a routing system for an AI Business Analyst.

Classify the question into exactly one:
RAG
SQL
BOTH

RAG: Use RAG for questions about:
- company information
- business policies
- operational procedures
- vendor rules
- strategy
- qualitative knowledge

SQL: Use SQL for questions about:
- revenue
- attendees
- counts
- averages
- rankings
- satisfaction
- lead conversion
- vendor metrics

BOTH: Use BOTH when the question needs:
1. Numerical business data
AND
2. Business knowledge/context

QUESTION:
{question}

Return ONLY one word: RAG, SQL, or BOTH.
"""
    response = llm.invoke(prompt)
    category = response.content.strip().upper()

    if "BOTH" in category:
        return "BOTH"
    elif "SQL" in category:
        return "SQL"
    else:
        return "RAG"

def generate_sql(question: str, api_key: str = None) -> str:
    """
    Generates a valid SQLite SQL query from a user question.
    """
    llm = get_llm(api_key)
    prompt = f"""
You are an expert SQLite data analyst.

DATABASE SCHEMA:
{DATABASE_SCHEMA}

Generate ONLY a valid SQLite SQL query to answer the user's question.

RULES:
- Return only SQL query string.
- No markdown code blocks.
- No explanation or extra prose.
- Use only the provided tables (events, vendors, monthly_summary).
- Use only the provided columns.
- Use SUM for total revenue.
- Use AVG for averages.
- Use COUNT for counting.
- Use GROUP BY for comparisons.
- Use ORDER BY for rankings.

USER QUESTION:
{question}
"""
    response = llm.invoke(prompt)
    sql = response.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def rag_answer(question: str, api_key: str = None) -> Tuple[str, list]:
    """
    Executes PDF RAG retrieval and synthesizes qualitative answer.
    """
    llm = get_llm(api_key)
    docs = retrieve_documents(question, k=4)
    context = create_context(docs)

    prompt = f"""
You are an expert AI Business Analyst for an Indian event management company.

Answer the user's question using ONLY the provided business documents.

IMPORTANT RULES:
1. Do not invent facts or numbers.
2. Do not use outside knowledge.
3. If information is unavailable, clearly say so.
4. Provide useful business insights.

Return formatted markdown:
## Answer

## Key Insights

## Business Implications

KNOWLEDGE BASE:
{context}

USER QUESTION:
{question}
"""
    response = llm.invoke(prompt)
    return response.content, docs

def sql_answer(question: str, api_key: str = None) -> Tuple[str, str, Any]:
    """
    Generates and executes SQL query, then formats answer using LLM.
    """
    llm = get_llm(api_key)
    # Ensure database is initialized
    init_database()

    sql = generate_sql(question, api_key)
    result = execute_sql(sql)

    if isinstance(result, str): # Error string
        return result, sql, None

    result_text = result.to_string(index=False)
    prompt = f"""
You are a senior Business Analyst.

Answer the user's question using ONLY the SQL result.

QUESTION:
{question}

SQL QUERY:
{sql}

QUERY RESULT:
{result_text}

Return formatted markdown:
## Answer

## Key Insights

## Business Implications

RULES:
- Do not invent numbers.
- Use only the data in the result table.
"""
    response = llm.invoke(prompt)
    return response.content, sql, result

def ai_analyst(question: str, api_key: str = None) -> Dict[str, Any]:
    """
    Main entry point for AI Analyst query pipeline.
    """
    init_database()
    route = classify_question(question, api_key)

    response_dict = {
        "route": route,
        "answer": "",
        "sql": "",
        "result": None,
        "sources": []
    }

    if route == "RAG":
        answer, docs = rag_answer(question, api_key)
        response_dict["answer"] = answer
        response_dict["sources"] = docs

    elif route == "SQL":
        answer, sql, result_df = sql_answer(question, api_key)
        response_dict["answer"] = answer
        response_dict["sql"] = sql
        response_dict["result"] = result_df

    elif route == "BOTH":
        sql_query = generate_sql(question, api_key)
        sql_result_df = execute_sql(sql_query)

        sql_result_text = ""
        if isinstance(sql_result_df, pd.DataFrame):
            sql_result_text = sql_result_df.to_string(index=False)
        else:
            sql_result_text = f"Error executing SQL: {sql_result_df}"

        retrieved_docs = retrieve_documents(question, k=4)
        rag_context = create_context(retrieved_docs)

        llm = get_llm(api_key)
        combined_prompt = f"""
You are an expert AI Business Analyst for an Indian event management company.

Answer the user's question by combining information from the provided SQL result and business documents.

IMPORTANT RULES:
1. Do not invent facts or numbers.
2. If information is unavailable, clearly say so.
3. Provide useful business insights.

Return formatted markdown:
## Answer

## Data-Driven Insights

## Business Context & Playbook Guidelines

## Strategic Recommendations

SQL QUERY:
{sql_query}

SQL RESULT:
{sql_result_text}

KNOWLEDGE BASE:
{rag_context}

USER QUESTION:
{question}
"""
        final_answer = llm.invoke(combined_prompt).content

        response_dict["answer"] = final_answer
        response_dict["sql"] = sql_query
        response_dict["result"] = sql_result_df
        response_dict["sources"] = retrieved_docs

    return response_dict
