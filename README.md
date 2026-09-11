# 🤖 AI Analyst: RAG & Text-to-SQL Powered Business Intelligence System

An end-to-end AI Analyst designed for event management intelligence. It unifies structured business data (Excel / SQLite databases) with unstructured documentation (PDF business reports & operational playbooks) using a **Hybrid Query Router**, **Text-to-SQL Engine**, **RAG Pipeline**, and an interactive **Gradio Dashboard**.

---

## 📌 Problem & Objective

Event management companies generate vast amounts of structured and unstructured business data across event records, vendor performance, monthly revenue summaries, operational playbooks, and strategic policy guidelines. 

Manually sifting through spreadsheets and PDF reports to answer business questions is slow and error-prone. The **AI Analyst** addresses this by:
- Automatically converting natural-language business questions into valid SQL queries.
- Executing semantic search over operational and business PDFs.
- Combining tabular query results with PDF context to deliver grounded, actionable insights.

---

## 🏗️ Architecture & Workflow

```
                        ┌──────────────────────────────┐
                        │   User Business Question     │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │     Intent Classifier        │
                        └──────┬───────┬───────┬───────┘
                               │       │       │
            ┌──────────────────┘       │       └──────────────────┐
            ▼                          ▼                          ▼
  ┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
  │   Text-to-SQL     │      │   Hybrid Engine   │      │     PDF RAG       │
  │     (SQLite)      │      │ (SQL + Context)   │      │  (FAISS Vector)   │
  └─────────┬─────────┘      └─────────┬─────────┘      └─────────┬─────────┘
            │                          │                          │
            └──────────────────┐       │       ┌──────────────────┘
                               ▼       ▼       ▼
                        ┌──────────────────────────────┐
                        │   Llama 3.3 70B (Groq LLM)   │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │  Gradio Web UI Dashboard     │
                        └──────────────────────────────┘
```

### Core Components
1. **Data Ingestion & Database Creation**: Loads `Event_Management_AI_Analyst_Data.xlsx` (sheets: `Events`, `Vendors`, `Monthly_Summary`) into an in-memory SQLite database using `Pandas` and `SQLAlchemy`.
2. **Text-to-SQL Engine**: Dynamically inspects database schema and generates SQL queries using LLM prompts, executes them safely, and returns DataFrame results.
3. **RAG Vector Pipeline**: Loads PDF documents (`Event_Management_Business_Reports.pdf`, `Event_Management_Operations_Playbook.pdf`), splits text using `RecursiveCharacterTextSplitter`, creates vector embeddings with `sentence-transformers/all-MiniLM-L6-v2`, and stores them in a `FAISS` vector store.
4. **Hybrid Query Router**: Classifies incoming queries into `SQL`, `Unstructured`, or `Hybrid` categories and passes data to the appropriate processing pipeline.
5. **Gradio Dashboard**: Interactive Web UI displaying synthesized AI answers, classification routing details, generated raw SQL, data tables, and document citations.

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **LLM**: `llama-3.3-70b-versatile` via LangChain Groq (`ChatGroq`)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (`HuggingFaceEmbeddings`)
- **Vector Index**: `FAISS` (Facebook AI Similarity Search)
- **Document Processors**: `PyPDFLoader`, `RecursiveCharacterTextSplitter` (LangChain)
- **Database & Data Processing**: `Pandas`, `SQLite3`, `OpenPyXL`, `SQLAlchemy`
- **UI Framework**: `Gradio`

---

## 📁 Repository Structure

```text
chatbot/
├── AI Analyst.ipynb                       # Main Jupyter Notebook with complete implementation & Gradio UI
├── Event_Management_AI_Analyst_Data.xlsx  # Multi-sheet Excel data (Events, Vendors, Monthly Summary)
├── Event_Management_Business_Reports.pdf  # PDF business performance reports
├── Event_Management_Operations_Playbook.pdf # PDF operational playbooks & guidelines
└── README.md                              # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure Python 3.10+ is installed on your machine.

### 2. Install Required Packages
```bash
pip install -U \
    langchain \
    langchain-community \
    langchain-text-splitters \
    langchain-huggingface \
    langchain-groq \
    faiss-cpu \
    sentence-transformers \
    pypdf \
    openpyxl \
    sqlalchemy \
    gradio \
    pandas
```

### 3. Set Groq API Key
Generate an API key from [Groq Console](https://console.groq.com/) and set it in your environment:

- **Windows (PowerShell)**:
  ```powershell
  $env:GROQ_API_KEY="your_groq_api_key_here"
  ```
- **Linux / macOS**:
  ```bash
  export GROQ_API_KEY="your_groq_api_key_here"
  ```

### 4. Run the Notebook
Launch Jupyter Notebook / VS Code and run `AI Analyst.ipynb`. The final cell launches the Gradio Web Interface locally at `http://127.0.0.1:7860`.

---

## 💡 Example Queries

| Question Type | Example Prompt | Engine Used |
| :--- | :--- | :--- |
| **Structured Data** | *"Which city generated the highest total revenue?"* | Text-to-SQL |
| **Structured Data** | *"List the top 3 vendors by rating and their contact details."* | Text-to-SQL |
| **Unstructured Document** | *"What are the key operational guidelines for venue setup?"* | RAG (FAISS) |
| **Hybrid Analysis** | *"Compare corporate event revenue against weddings, and suggest strategic improvements based on our business reports."* | Hybrid (SQL + RAG) |

---

## 📜 License
This project is for demonstration and research purposes.
