import pandas as pd


def generate_market_insights(df: pd.DataFrame):

    df = df.copy()
    df = df[df["ticker"] != "UNKNOWN"].copy()

    # ---------------------------------
    # Market Mood
    # ---------------------------------

    avg_sentiment = df["sentiment_score"].mean()

    if avg_sentiment >= 70:
        market_mood = "Bullish"

    elif avg_sentiment >= 45:
        market_mood = "Neutral"

    else:
        market_mood = "Bearish"

    # ---------------------------------
    # Top Opportunity
    # ---------------------------------

    top_opportunity = df.loc[
        df["opportunity_score"].idxmax()
    ]

    # ---------------------------------
    # Highest Risk
    # ---------------------------------

    highest_risk = df.loc[
        df["risk_score"].idxmax()
    ]

    # ---------------------------------
    # Most Discussed
    # ---------------------------------

    most_discussed = df.loc[
        df["total_news"].idxmax()
    ]

    # ---------------------------------
    # Lowest Confidence
    # ---------------------------------

    weakest_signal = df.loc[
        df["confidence_score"].idxmin()
    ]

    # ---------------------------------
    # Analyst Priorities
    # ---------------------------------

    priorities = (
        df.sort_values(
            "opportunity_score",
            ascending=False
        )
        .head(3)["ticker"]
        .tolist()
    )

    analyst_priority = ", ".join(priorities)

    # ---------------------------------
    # Executive Brief
    # ---------------------------------

    executive_brief = (
        f"Overall market sentiment remains {market_mood.lower()}. "
        f"{top_opportunity['ticker']} currently leads the opportunity rankings with an "
        f"opportunity score of {top_opportunity['opportunity_score']:.1f} and "
        f"{top_opportunity['confidence_level'].lower()} confidence. "
        f"{highest_risk['ticker']} presents the highest risk with a risk score of "
        f"{highest_risk['risk_score']:.1f}. "
        f"{most_discussed['ticker']} attracted the greatest media attention "
        f"({int(most_discussed['total_news'])} news articles). "
        f"Analysts should prioritize: {analyst_priority}."
    )

    return pd.DataFrame([
    {
        "market_mood": market_mood,

        "executive_brief": executive_brief,

        "key_takeaways":
            f"{top_opportunity['ticker']} shows the strongest opportunity while "
            f"{highest_risk['ticker']} requires close monitoring.",

        "priority_companies": analyst_priority,

        "analyst_questions":
            f"Why is {highest_risk['ticker']} carrying elevated risk and can "
            f"{top_opportunity['ticker']} sustain its momentum?",

        "suggested_focus":
            "Monitor sentiment shifts, validate high-opportunity signals, and "
            "watch changes in market confidence.",

        "top_opportunity": top_opportunity["ticker"],

        "highest_risk": highest_risk["ticker"],

        "most_discussed": most_discussed["ticker"],

        "weakest_signal": weakest_signal["ticker"]
    }
])