import sqlite3
import pandas as pd
from pathlib import Path

# ---------------------------------------------
# Paths
# ---------------------------------------------

WAREHOUSE = Path("data/warehouse/analytics.db")

EXPORT_FOLDER = Path("dashboard_data")
EXPORT_FOLDER.mkdir(exist_ok=True)

# ---------------------------------------------
# Tables required by Power BI
# ---------------------------------------------

TABLES = [
    "company_metrics",
    "company_intelligence",
    "market_insights",
    "news",
    "prices",
    "sentiment"
]

# ---------------------------------------------
# Export
# ---------------------------------------------

conn = sqlite3.connect(WAREHOUSE)

for table in TABLES:

    print(f"Exporting {table}...")

    df = pd.read_sql(
        f"SELECT * FROM {table}",
        conn
    )

    output_file = EXPORT_FOLDER / f"{table}.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print(f"OK {table}.csv")

conn.close()

print("\n===================================")
print("Dashboard export completed.")
print("===================================")
