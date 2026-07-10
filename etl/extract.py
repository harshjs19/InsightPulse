import sqlite3

import pandas as pd

from config.settings import RAW_DATA_DIR


SNAPSHOT_DB = RAW_DATA_DIR / "market_latest.db"


def extract_table(table_name: str) -> pd.DataFrame:
    """Extract a table from the latest database snapshot."""

    with sqlite3.connect(SNAPSHOT_DB) as conn:
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql_query(query, conn)


def extract_all():
    """Extract all source tables."""

    return {
        "news": extract_table("news"),
        "prices": extract_table("prices"),
        "sentiment": extract_table("sentiment"),
    }