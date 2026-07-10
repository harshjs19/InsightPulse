import sqlite3
import pandas as pd


def save_market_insights(df: pd.DataFrame):

    conn = sqlite3.connect(
        "data/warehouse/analytics.db"
    )

    df.to_sql(
        "market_insights",
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()
    conn.close()

    print(
        "Market Insights saved successfully."
    )