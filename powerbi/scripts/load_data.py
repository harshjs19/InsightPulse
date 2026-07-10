import sqlite3
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Locate analytics.db automatically
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "data" / "warehouse" / "analytics.db"

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found:\n{DB_PATH}")

# --------------------------------------------------
# Connect
# --------------------------------------------------

conn = sqlite3.connect(DB_PATH)

# --------------------------------------------------
# Load Tables
# --------------------------------------------------

company_intelligence = pd.read_sql(
    "SELECT * FROM company_intelligence",
    conn
)

company_metrics = pd.read_sql(
    "SELECT * FROM company_metrics",
    conn
)

market_insights = pd.read_sql(
    "SELECT * FROM market_insights",
    conn
)

news = pd.read_sql(
    "SELECT * FROM news",
    conn
)

prices = pd.read_sql(
    "SELECT * FROM prices",
    conn
)

sentiment = pd.read_sql(
    "SELECT * FROM sentiment",
    conn
)

conn.close()

print("Data loaded successfully.")