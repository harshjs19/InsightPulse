import pandas as pd


def build_insights(df: pd.DataFrame):

    df = df.copy()

    executive_summary = []
    analyst_insight = []
    business_impact = []
    suggested_action = []
    key_drivers = []

    for _, row in df.iterrows():

        drivers = []

        # -------------------------
        # Sentiment
        # -------------------------

        if row["sentiment_score"] >= 75:
            drivers.append("Positive Sentiment")
        elif row["sentiment_score"] <= 35:
            drivers.append("Negative Sentiment")

        # -------------------------
        # Attention
        # -------------------------

        if row["attention_score"] >= 70:
            drivers.append("High Attention")
        elif row["attention_score"] <= 30:
            drivers.append("Low Attention")

        # -------------------------
        # Confidence
        # -------------------------

        drivers.append(
            f'{row["confidence_level"]} Confidence'
        )

        # -------------------------
        # Risk
        # -------------------------

        if row["risk_level"] == "High":
            drivers.append("High Risk")

        # -------------------------
        # Opportunity
        # -------------------------

        if row["opportunity_level"] == "High":
            drivers.append("High Opportunity")

        key_drivers.append(
            ", ".join(drivers)
        )

        # =======================================
        # Executive Summary
        # =======================================

        if row["recommendation"] == "Strong Opportunity":

            executive_summary.append(
                f'{row["ticker"]} exhibits one of the strongest market signals in the current dataset.'
            )

        elif row["recommendation"] == "Opportunity":

            executive_summary.append(
                f'{row["ticker"]} shows favorable conditions supported by positive market intelligence.'
            )

        elif row["recommendation"] == "High Risk":

            executive_summary.append(
                f'{row["ticker"]} is experiencing elevated market risk based on current intelligence.'
            )

        elif row["recommendation"] == "Caution":

            executive_summary.append(
                f'{row["ticker"]} shows emerging risk signals that warrant closer attention.'
            )

        elif row["recommendation"] == "Watchlist":

            executive_summary.append(
                f'{row["ticker"]} should remain on the analyst watchlist.'
            )

        else:

            executive_summary.append(
                f'{row["ticker"]} currently shows no exceptional market behaviour.'
            )

        # =======================================
        # Analyst Insight
        # =======================================

        analyst_insight.append(
            f'Current recommendation is "{row["recommendation"]}" supported by {row["confidence_level"].lower()} confidence.'
        )

        # =======================================
        # Business Impact
        # =======================================

        if row["risk_level"] == "High":

            business_impact.append(
                "Negative developments may require closer monitoring."
            )

        elif row["opportunity_level"] == "High":

            business_impact.append(
                "Current conditions justify deeper market investigation."
            )

        else:

            business_impact.append(
                "No significant business impact detected at present."
            )

        # =======================================
        # Suggested Action
        # =======================================

        if row["recommendation"] == "Strong Opportunity":

            suggested_action.append(
                "Review recent news and prioritize for deeper research."
            )

        elif row["recommendation"] == "Opportunity":

            suggested_action.append(
                "Review recent news and monitor further developments."
            )

        elif row["recommendation"] == "High Risk":

            suggested_action.append(
                "Monitor upcoming news closely for additional negative signals."
            )

        elif row["recommendation"] == "Caution":

            suggested_action.append(
                "Review risk factors and assess exposure."
            )

        elif row["recommendation"] == "Insufficient Data":

            suggested_action.append(
                "Wait for additional market information before drawing conclusions."
            )

        else:

            suggested_action.append(
                "Continue routine monitoring."
            )

    df["executive_summary"] = executive_summary
    df["analyst_insight"] = analyst_insight
    df["business_impact"] = business_impact
    df["suggested_action"] = suggested_action
    df["key_drivers"] = key_drivers

    return df