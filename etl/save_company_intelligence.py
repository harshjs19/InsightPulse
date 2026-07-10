import sqlite3
import pandas as pd


def save_company_intelligence(df: pd.DataFrame):

    conn = sqlite3.connect(
        "data/warehouse/analytics.db"
    )

    df.to_sql(
        "company_intelligence",
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()
    conn.close()

    print(
        "Company Intelligence saved successfully."
    )