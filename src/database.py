import sqlite3
import pandas as pd
from pathlib import Path
from src.config import EXCEL_FILE, DB_PATH

DATABASE_SCHEMA = """
TABLE: events
Columns:
Event_ID (TEXT)
City (TEXT)
Event_Type (TEXT)
Event_Name (TEXT)
Event_Date (DATE)
Client (TEXT)
Revenue_INR (INTEGER)
Attendees (INTEGER)
Satisfaction_Pct (FLOAT)
Lead_Conversion_Pct (FLOAT)

TABLE: vendors
Columns:
Vendor_ID (TEXT)
Vendor_Name (TEXT)
Category (TEXT)
Base_City (TEXT)
Rating (FLOAT)
Events_Handled (INTEGER)
On_Time_Pct (FLOAT)

TABLE: monthly_summary
Columns:
Month (TEXT)
Events (INTEGER)
Revenue_INR (INTEGER)
Avg_Satisfaction_Pct (FLOAT)
Avg_Lead_Conversion_Pct (FLOAT)
"""

def init_database(excel_path: Path = EXCEL_FILE, db_path: Path = DB_PATH, force_reload: bool = False):
    """
    Loads sheets from Excel and creates or replaces SQLite database tables.
    """
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel data file not found at {excel_path}")

    # Check if DB already exists and has tables
    if db_path.exists() and not force_reload:
        try:
            conn = sqlite3.connect(str(db_path))
            tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
            conn.close()
            if len(tables) >= 3:
                return str(db_path)
        except Exception:
            pass

    conn = sqlite3.connect(str(db_path))

    # Read sheets
    events_df = pd.read_excel(excel_path, sheet_name="Events")
    vendors_df = pd.read_excel(excel_path, sheet_name="Vendors")
    monthly_df = pd.read_excel(excel_path, sheet_name="Monthly_Summary")

    # Save to SQLite
    events_df.to_sql("events", conn, if_exists="replace", index=False)
    vendors_df.to_sql("vendors", conn, if_exists="replace", index=False)
    monthly_df.to_sql("monthly_summary", conn, if_exists="replace", index=False)

    conn.close()
    return str(db_path)

def execute_sql(query: str, db_path: Path = DB_PATH):
    """
    Executes a SQL query safely and returns a DataFrame or an error string.
    """
    try:
        conn = sqlite3.connect(str(db_path))
        result_df = pd.read_sql_query(query, conn)
        conn.close()
        return result_df
    except Exception as e:
        return f"SQL Execution Error: {str(e)}"

def get_database_summary(db_path: Path = DB_PATH) -> dict:
    """
    Returns quick metric summary from database tables.
    """
    init_database(db_path=db_path)
    try:
        conn = sqlite3.connect(str(db_path))
        total_events = pd.read_sql_query("SELECT COUNT(*) as count FROM events", conn).iloc[0]['count']
        total_revenue = pd.read_sql_query("SELECT SUM(Revenue_INR) as total FROM events", conn).iloc[0]['total']
        total_vendors = pd.read_sql_query("SELECT COUNT(*) as count FROM vendors", conn).iloc[0]['count']
        top_city = pd.read_sql_query("SELECT City, SUM(Revenue_INR) as rev FROM events GROUP BY City ORDER BY rev DESC LIMIT 1", conn).iloc[0]['City']
        conn.close()
        return {
            "total_events": total_events,
            "total_revenue": total_revenue,
            "total_vendors": total_vendors,
            "top_city": top_city
        }
    except Exception:
        return {
            "total_events": 0,
            "total_revenue": 0,
            "total_vendors": 0,
            "top_city": "N/A"
        }
