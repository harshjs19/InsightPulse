import pandas as pd


def _transform_news(news_df: pd.DataFrame) -> pd.DataFrame:
    news_df = news_df.copy()

    news_df = news_df.drop_duplicates(subset="title")

    news_df["published_at"] = pd.to_datetime(
        news_df["published_at"],
        errors="coerce"
    )

    news_df = news_df.sort_values(
        by="published_at",
        ascending=False
    )

    return news_df.reset_index(drop=True)


def _transform_prices(prices_df: pd.DataFrame) -> pd.DataFrame:
    prices_df = prices_df.copy()

    prices_df["date"] = pd.to_datetime(
        prices_df["date"],
        errors="coerce"
    )

    prices_df = prices_df.sort_values(
        by=["symbol", "date"]
    )

    return prices_df.reset_index(drop=True)


def _transform_sentiment(sentiment_df: pd.DataFrame) -> pd.DataFrame:
    sentiment_df = sentiment_df.copy()

    sentiment_df = sentiment_df.drop_duplicates()

    sentiment_df["sentiment_score"] = pd.to_numeric(
        sentiment_df["sentiment_score"],
        errors="coerce"
    )

    sentiment_df["analyzed_at"] = pd.to_datetime(
        sentiment_df["analyzed_at"],
        errors="coerce"
    )

    sentiment_df = sentiment_df.sort_values(
        by="analyzed_at",
        ascending=False
    )

    return sentiment_df.reset_index(drop=True)


def transform_all(tables: dict) -> dict:
    return {
        "news": _transform_news(tables["news"]),
        "prices": _transform_prices(tables["prices"]),
        "sentiment": _transform_sentiment(tables["sentiment"]),
    }