import os
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# Ensure root directory is in python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import get_groq_api_key
from src.database import get_database_summary
from src.vectorstore import format_sources
from src.engine import ai_analyst

# Page Configuration
st.set_page_config(
    page_title="AI Analyst | Event Management Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphism CSS & Aesthetic Design
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header Gradient */
    .header-title {
        background: linear-gradient(90deg, #a855f7, #6366f1, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
    }
    
    .header-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(168, 85, 247, 0.4);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Route Badges */
    .badge-sql {
        background: linear-gradient(135deg, #0284c7, #0369a1);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-rag {
        background: linear-gradient(135deg, #059669, #047857);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-both {
        background: linear-gradient(135deg, #7c3aed, #6d28d9);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }

    /* Output Card */
    .output-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    /* Hide Default Footer */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/isometric-line/100/combo-chart.png", width=64)
    st.title("🤖 AI Analyst")
    st.markdown("**Hybrid Text-to-SQL & RAG Engine**")
    st.divider()

    # Groq API Key Setup
    env_api_key = get_groq_api_key()
    user_api_key = st.text_input(
        "Groq API Key",
        value=env_api_key,
        type="password",
        help="Get a free API key at https://console.groq.com"
    )

    api_key_to_use = user_api_key.strip() if user_api_key else env_api_key

    if api_key_to_use:
        st.success("✅ Groq API Key Configured")
    else:
        st.warning("⚠️ Groq API Key required")

    st.divider()
    st.markdown("### 🛠️ Architecture")
    st.markdown("""
    - **LLM**: Llama 3.3 70B (Groq)
    - **Embeddings**: MiniLM-L6-v2
    - **Vector Store**: FAISS
    - **Database**: SQLite (Events Data)
    """)
    st.divider()
    st.caption("Developed for Event Management Intelligence")

# Main Header Section
st.markdown('<div class="header-title">🤖 AI Business Analyst</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Unified Event Analytics with Text-to-SQL Data Queries & Document RAG Synthesis</div>', unsafe_allow_html=True)

# KPI Summary Row
db_metrics = get_database_summary()
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Events</div>
        <div class="metric-value">{db_metrics['total_events']}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    rev_formatted = f"₹{db_metrics['total_revenue']/1e7:.2f} Cr" if db_metrics['total_revenue'] > 0 else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">{rev_formatted}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Registered Vendors</div>
        <div class="metric-value">{db_metrics['total_vendors']}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Top Revenue City</div>
        <div class="metric-value">{db_metrics['top_city']}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# Sample Query Selector
sample_queries = [
    "Select a sample question...",
    "Which city generated the highest revenue?",
    "List the top 3 vendors by rating and their contact details.",
    "What are the vendor selection criteria?",
    "What are the key operational guidelines for venue setup?",
    "Which event type generates the most revenue and what strategy should management use?",
    "Identify high-revenue events with relatively low satisfaction.",
    "Give management 5 recommendations based on the business data."
]

selected_sample = st.selectbox("💡 Quick Sample Questions", sample_queries)

# User Query Input Form
with st.form("query_form", clear_on_submit=False):
    default_query_value = "" if selected_sample == "Select a sample question..." else selected_sample
    user_query = st.text_area("Ask AI Analyst a business question:", value=default_query_value, height=100, placeholder="e.g. Which city generated the highest total revenue?")
    
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        submit_button = st.form_submit_button("🤖 Analyze", type="primary", use_container_width=True)

# Analysis Execution
if submit_button and user_query.strip():
    if not api_key_to_use:
        st.error("❌ Please provide a valid Groq API Key in the sidebar to run analysis.")
    else:
        with st.spinner("🔍 Routing question, querying database & analyzing document context..."):
            try:
                res = ai_analyst(user_query, api_key=api_key_to_use)
                
                st.markdown("### 📊 Analysis Results")
                
                # Display Route Badge
                route = res.get("route", "UNKNOWN")
                if route == "SQL":
                    st.markdown('<span class="badge-sql">🔀 Route: Structured Data (Text-to-SQL Engine)</span>', unsafe_allow_html=True)
                elif route == "RAG":
                    st.markdown('<span class="badge-rag">🔀 Route: Unstructured Documents (FAISS PDF RAG)</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-both">🔀 Route: Hybrid Analysis (SQL Data + RAG Context)</span>', unsafe_allow_html=True)

                st.write("")

                # Main Answer Tabs
                tab_answer, tab_sql, tab_data, tab_sources = st.tabs([
                    "🤖 Synthesized Answer", 
                    "💻 Generated SQL", 
                    "📈 Data Table & Charts", 
                    "📚 Document Citations"
                ])

                with tab_answer:
                    st.markdown(res.get("answer", "No answer generated."))

                with tab_sql:
                    sql_text = res.get("sql", "")
                    if sql_text:
                        st.code(sql_text, language="sql")
                    else:
                        st.info("No SQL query generated for this document-only RAG route.")

                with tab_data:
                    data_df = res.get("result")
                    if isinstance(data_df, pd.DataFrame) and not data_df.empty:
                        st.dataframe(data_df, use_container_width=True)
                        
                        # Plotly Auto-visualization
                        num_cols = data_df.select_dtypes(include=['number']).columns.tolist()
                        cat_cols = data_df.select_dtypes(include=['object', 'category']).columns.tolist()
                        
                        if cat_cols and num_cols:
                            st.subheader("📊 Visual Insights")
                            cat_col = cat_cols[0]
                            num_col = num_cols[0]
                            fig = px.bar(
                                data_df, 
                                x=cat_col, 
                                y=num_col, 
                                title=f"{num_col} by {cat_col}",
                                color=cat_col,
                                template="plotly_dark"
                            )
                            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No tabular dataset returned for this query.")

                with tab_sources:
                    sources_list = res.get("sources", [])
                    if sources_list:
                        formatted_s = format_sources(sources_list)
                        st.markdown(formatted_s)
                        with st.expander("🔍 View Raw Source Chunks"):
                            for i, doc in enumerate(sources_list):
                                page = doc.metadata.get("page", 0) + 1
                                src = Path(doc.metadata.get("source", "Doc")).name
                                st.markdown(f"**Chunk {i+1}** ({src}, Page {page}):")
                                st.text(doc.page_content)
                                st.divider()
                    else:
                        st.info("No PDF document citations retrieved for this query.")

            except Exception as e:
                st.error(f"❌ Error during execution: {str(e)}")

st.divider()
st.caption("AI Analyst v1.0 • Powered by LangChain, Groq Llama 3.3 70B, FAISS, SQLite, and Streamlit")
