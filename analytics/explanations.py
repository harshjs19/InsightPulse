import pandas as pd


def generate_explanation(row):

    reasons = []

    # -----------------------------
    # Sentiment
    # -----------------------------

    if row["sentiment_score"] >= 75:
        reasons.append(
            "Market sentiment is strongly positive."
        )

    elif row["sentiment_score"] <= 35:
        reasons.append(
            "Market sentiment is strongly negative."
        )

    # -----------------------------
    # Attention
    # -----------------------------

    if row["attention_score"] >= 70:
        reasons.append(
            "Media attention is significantly above normal."
        )

    elif row["attention_score"] <= 30:
        reasons.append(
            "Current media attention is relatively low."
        )

    # -----------------------------
    # Confidence
    # -----------------------------

    if row["confidence_score"] >= 80:
        reasons.append(
            "Insights are supported by a large volume of news."
        )

    elif row["confidence_score"] <= 20:
        reasons.append(
            "Very limited news coverage reduces confidence."
        )

    # -----------------------------
    # Risk
    # -----------------------------

    if row["risk_score"] >= 75:
        reasons.append(
            "Risk indicators remain elevated."
        )

    # -----------------------------
    # Opportunity
    # -----------------------------

    if row["opportunity_score"] >= 75:
        reasons.append(
            "Current signals indicate strong research potential."
        )

    if not reasons:

        reasons.append(
            "No significant market signals detected."
        )

    return " ".join(reasons)


def build_explanations(df: pd.DataFrame):

    df = df.copy()

    df["explanation"] = df.apply(
        generate_explanation,
        axis=1
    )

    return df