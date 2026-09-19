import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Base Directory of Project
BASE_DIR = Path(__file__).resolve().parent.parent

# Data Files
EXCEL_FILE = BASE_DIR / "Event_Management_AI_Analyst_Data.xlsx"
BUSINESS_REPORT = BASE_DIR / "Event_Management_Business_Reports.pdf"
OPERATIONS_REPORT = BASE_DIR / "Event_Management_Operations_Playbook.pdf"

# Database & Vector Index Locations
DB_PATH = BASE_DIR / "event_management.db"
FAISS_INDEX_DIR = BASE_DIR / "event_management_faiss"

# Model Configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"

def get_groq_api_key() -> str:
    """Retrieve Groq API key from environment variable."""
    return os.getenv("GROQ_API_KEY", "").strip()
