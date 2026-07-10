import pandas as pd


def build_company_metrics(tables: dict) -> pd.DataFrame:
    news = tables["news"]
    sentiment = tables["sentiment"]
    prices = tables["prices"]

    sentiment_summary = (
        sentiment.groupby("ticker")
        .agg(
            total_news=("ticker", "count"),
            avg_sentiment=("sentiment_value", "mean"),
            positive_news=("sentiment_label", lambda x: (x == "positive").sum()),
            neutral_news=("sentiment_label", lambda x: (x == "neutral").sum()),
            negative_news=("sentiment_label", lambda x: (x == "negative").sum()),
            avg_confidence=("sentiment_score", "mean"),
        )
        .reset_index()
    )

    price_summary = (
        prices.groupby("symbol")
        .agg(
            latest_price=("close_price", "last"),
            avg_price=("close_price", "mean"),
            avg_volume=("volume", "mean"),
        )
        .reset_index()
        .rename(columns={"symbol": "ticker"})
    )

    metrics = sentiment_summary.merge(
        price_summary,
        on="ticker",
        how="left"
    )

    return metrics