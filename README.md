# 🤖 AI Analyst: RAG & Text-to-SQL Powered Business Intelligence System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-FF4B4B.svg)](https://streamlit.io)
[![Gradio](https://img.shields.io/badge/Gradio-4.19%2B-orange.svg)](https://gradio.app)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green.svg)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/LLM-Llama_3.3_70B-purple.svg)](https://groq.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7.svg)](https://render.com)
[![AWS](https://img.shields.io/badge/Deploy-AWS_App_Runner-FF9900.svg)](https://aws.amazon.com/)

An enterprise-grade **AI Business Analyst** designed for event management intelligence. It unifies structured business data (Excel / SQLite databases) with unstructured documentation (PDF business reports & operational playbooks) using a **Hybrid Query Router**, **Text-to-SQL Engine**, **RAG Vector Pipeline**, and interactive **Streamlit & Gradio Dashboards**.

---

## 🏗️ Architecture & Workflow

```text
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
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
  ┌───────────────────────────┐                 ┌───────────────────────────┐
  │   Streamlit Web Dashboard │                 │    Gradio Web Dashboard   │
  │     (Port 8501 / Cloud)   │                 │     (Port 7860 / Docker)  │
  └───────────────────────────┘                 └───────────────────────────┘
```

### Core Components
1. **Data Ingestion & SQLite Database (`src/database.py`)**: Automatically ingests `Event_Management_AI_Analyst_Data.xlsx` (sheets: `Events`, `Vendors`, `Monthly_Summary`) into an in-memory SQLite database (`event_management.db`).
2. **Text-to-SQL Engine (`src/engine.py`)**: Dynamically inspects database schema, translates natural language into optimized SQLite queries, executes safely, and extracts DataFrame results.
3. **PDF RAG Vector Store (`src/vectorstore.py`)**: Processes business & operational PDFs (`Event_Management_Business_Reports.pdf`, `Event_Management_Operations_Playbook.pdf`), splits text via `RecursiveCharacterTextSplitter`, creates dense embeddings with `sentence-transformers/all-MiniLM-L6-v2`, and retrieves relevant context with `FAISS`.
4. **Hybrid Router & LLM Synthesizer (`src/engine.py`)**: Classifies queries into `SQL`, `RAG`, or `BOTH` and synthesizes comprehensive business recommendations using **Llama 3.3 70B (Groq)**.
5. **Interactive Web Dashboards (`streamlit_app.py` & `app.py`)**:
   - **Streamlit**: Glassmorphism UI, KPI cards, auto-visualization with **Plotly** charts, SQL syntax code viewer, RAG citations, and sample question pills.
   - **Gradio**: Modern tabbed interface with clean input controls.

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **LLM**: `llama-3.3-70b-versatile` via `langchain-groq`
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (`HuggingFaceEmbeddings`)
- **Vector Search**: `FAISS` (Facebook AI Similarity Search)
- **Database & Data Processing**: `SQLite3`, `Pandas`, `OpenPyXL`, `SQLAlchemy`
- **User Interfaces**: `Streamlit`, `Gradio`, `Plotly`
- **Containerization & Deployment**: `Docker`, `Docker Compose`, `Render`, `AWS App Runner`, `Streamlit Cloud`

---

## 📁 Repository Structure

```text
chatbot/
├── .streamlit/
│   └── config.toml                           # Streamlit visual theme configuration
├── deploy/
│   ├── render_deploy.md                      # Render deployment step-by-step guide
│   ├── streamlit_deploy.md                   # Streamlit Cloud deployment guide
│   └── aws_deploy.md                         # AWS App Runner & EC2 Docker guide
├── src/
│   ├── __init__.py                           # Package marker
│   ├── config.py                             # Configuration & path management
│   ├── database.py                           # SQLite & Excel data manager
│   ├── vectorstore.py                        # FAISS vector store manager
│   └── engine.py                             # Hybrid Intent Router & LLM pipeline
├── streamlit_app.py                          # Streamlit Dashboard application
├── app.py                                    # Gradio Dashboard application
├── AI Analyst.ipynb                          # Jupyter Notebook implementation
├── Event_Management_AI_Analyst_Data.xlsx     # Multi-sheet Excel data
├── Event_Management_Business_Reports.pdf     # PDF business report document
├── Event_Management_Operations_Playbook.pdf # PDF operational playbook document
├── Dockerfile                                # Production Docker container manifest
├── docker-compose.yml                        # Docker Compose configuration
├── render.yaml                               # Render Infrastructure-as-Code Blueprint
├── requirements.txt                          # Python production dependencies
├── .env.example                              # Environment variable template
└── README.md                                 # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Groq API Key (Get a free key from [Groq Console](https://console.groq.com/))

### 2. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/your-username/chatbot.git
cd chatbot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and insert your Groq API Key:
```bash
cp .env.example .env
```
Inside `.env`:
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

### 5. Launch Web Dashboards

#### 🌟 Option A: Launch Streamlit UI (Recommended)
```bash
streamlit run streamlit_app.py
```
Open your browser at `http://localhost:8501`.

#### ⚡ Option B: Launch Gradio UI
```bash
python app.py
```
Open your browser at `http://localhost:7860`.

---

## 🐳 Docker Container Execution

Build and launch the containerized application locally using Docker Compose:

```bash
# Build and run container
docker-compose up --build
```

- Streamlit Dashboard: `http://localhost:8501`
- Gradio Dashboard: `http://localhost:7860`

---

## ☁️ Deployment Guides

Detailed deployment instructions are available in the [`deploy/`](file:///d:/LLMs_RAG/chatbot/deploy/) directory:

- 🟣 **Render Deployment**: Read [`deploy/render_deploy.md`](file:///d:/LLMs_RAG/chatbot/deploy/render_deploy.md)
- 🎈 **Streamlit Community Cloud**: Read [`deploy/streamlit_deploy.md`](file:///d:/LLMs_RAG/chatbot/deploy/streamlit_deploy.md)
- ☁️ **AWS App Runner & EC2**: Read [`deploy/aws_deploy.md`](file:///d:/LLMs_RAG/chatbot/deploy/aws_deploy.md)

---

## 💡 Example Queries

| Question Type | Example Prompt | Pipeline Used |
| :--- | :--- | :--- |
| **Structured Data** | *"Which city generated the highest revenue?"* | Text-to-SQL |
| **Structured Data** | *"List the top 3 vendors by rating and their contact details."* | Text-to-SQL |
| **Unstructured Document** | *"What are the key operational guidelines for venue setup?"* | RAG (FAISS) |
| **Hybrid Analysis** | *"Which event type generates the most revenue and what strategy should management use?"* | Hybrid (SQL + RAG) |
| **Strategic Advisory** | *"Give management 5 recommendations based on the business data."* | Hybrid (SQL + RAG) |

---

## 📜 License
This project is for enterprise business intelligence demonstration and research purposes.
