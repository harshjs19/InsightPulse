import sqlite3

from config.settings import ANALYTICS_DB


def load_all(tables: dict):
    """Load transformed data into the analytics warehouse."""

    with sqlite3.connect(ANALYTICS_DB) as conn:
        for table_name, dataframe in tables.items():
            dataframe.to_sql(
                table_name,
                conn,
                if_exists="replace",
                index=False
            )