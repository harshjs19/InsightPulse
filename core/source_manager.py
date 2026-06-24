from pathlib import Path
import sqlite3

from config.settings import MARKET_DB


REQUIRED_TABLES = {"news", "prices", "sentiment"}


def _connect():
    return sqlite3.connect(MARKET_DB)


def validate_source():
    """Validate that the AlphaLens database is available."""

    if not MARKET_DB.exists():
        return {
            "valid": False,
            "error": f"Database not found: {MARKET_DB}"
        }

    return {
        "valid": True,
        "database": str(MARKET_DB)
    }


def list_tables():
    """Return all user tables."""

    with _connect() as conn:
        cursor = conn.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name != 'sqlite_sequence'
            ORDER BY name
        """)

        return [row[0] for row in cursor.fetchall()]


def get_schema():
    """Return schema information for every table."""

    schema = {}

    with _connect() as conn:

        for table in list_tables():

            cursor = conn.execute(f"PRAGMA table_info({table})")

            schema[table] = [
                column[1]
                for column in cursor.fetchall()
            ]

    return schema


def get_row_counts():
    """Return row counts for every table."""

    counts = {}

    with _connect() as conn:

        for table in list_tables():

            cursor = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            )

            counts[table] = cursor.fetchone()[0]

    return counts


def build_source_profile():
    """Build a summary profile of the source database."""

    tables = set(list_tables())

    return {
        "database": str(MARKET_DB),
        "tables": sorted(tables),
        "table_count": len(tables),
        "row_counts": get_row_counts(),
        "schema": get_schema(),
        "compatible": REQUIRED_TABLES.issubset(tables)
    }