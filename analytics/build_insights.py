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
        # Only flag when genuinely noteworthy — Medium is the
        # default state and adds no information.

        if row["confidence_level"] in ("Very High", "High"):
            drivers.append("High Confidence")
        elif row["confidence_level"] in ("Very Low", "Low"):
            drivers.append("Low Confidence")

        # -------------------------
        # Risk
        # -------------------------

        if row["risk_level"] == "High":
            drivers.append("High Risk")
        elif row["risk_level"] == "Moderate":
            drivers.append("Elevated Risk")

        # -------------------------
        # Opportunity
        # -------------------------

        if row["opportunity_level"] == "High":
            drivers.append("High Opportunity")
        elif row["opportunity_level"] == "Moderate":
            drivers.append("Moderate Opportunity")

        key_drivers.append(
            ", ".join(drivers) if drivers else "No exceptional signals"
        )

        # =======================================
        # Executive Summary
        # =======================================

        rec = row["recommendation"]

        if rec == "Strong Buy":

            executive_summary.append(
                f'{row["ticker"]} exhibits the strongest market signals '
                f'in the current dataset with high-conviction positive intelligence.'
            )

        elif rec == "Buy":

            executive_summary.append(
                f'{row["ticker"]} shows favorable conditions supported '
                f'by positive market intelligence and manageable risk.'
            )

        elif rec == "Accumulate":

            executive_summary.append(
                f'{row["ticker"]} displays a slight positive tilt in '
                f'current market signals, warranting gradual position building.'
            )

        elif rec == "Hold":

            executive_summary.append(
                f'{row["ticker"]} currently shows no exceptional '
                f'market signals in either direction.'
            )

        elif rec == "Reduce":

            executive_summary.append(
                f'{row["ticker"]} is showing risk signals that outweigh '
                f'current opportunity indicators.'
            )

        elif rec == "Sell":

            executive_summary.append(
                f'{row["ticker"]} is experiencing elevated market risk '
                f'with high-conviction negative intelligence.'
            )

        elif rec == "Insufficient Data":

            executive_summary.append(
                f'{row["ticker"]} lacks sufficient market coverage '
                f'to support a reliable recommendation.'
            )

        else:

            executive_summary.append(
                f'{row["ticker"]} currently shows no exceptional market behaviour.'
            )

        # =======================================
        # Analyst Insight
        # =======================================

        analyst_insight.append(
            f'Current recommendation is "{row["recommendation"]}" '
            f'supported by {row["confidence_level"].lower()} confidence.'
        )

        # =======================================
        # Business Impact
        # =======================================

        if row["risk_level"] == "High":

            business_impact.append(
                "Negative developments may require immediate attention "
                "and exposure review."
            )

        elif row["risk_level"] == "Moderate":

            business_impact.append(
                "Emerging risk signals warrant closer monitoring "
                "of upcoming developments."
            )

        elif row["opportunity_level"] == "High":

            business_impact.append(
                "Current conditions justify deeper market investigation "
                "and potential position initiation."
            )

        elif row["opportunity_level"] == "Moderate":

            business_impact.append(
                "Moderate opportunity signals suggest continued "
                "monitoring for strengthening trends."
            )

        else:

            business_impact.append(
                "No significant business impact detected at present."
            )

        # =======================================
        # Suggested Action
        # =======================================

        if rec == "Strong Buy":

            suggested_action.append(
                "Prioritize for deeper research and consider "
                "initiating or increasing position."
            )

        elif rec == "Buy":

            suggested_action.append(
                "Review recent news and monitor for position "
                "entry opportunities."
            )

        elif rec == "Accumulate":

            suggested_action.append(
                "Monitor developments and consider gradual "
                "position building on confirmation."
            )

        elif rec == "Hold":

            suggested_action.append(
                "Continue routine monitoring."
            )

        elif rec == "Reduce":

            suggested_action.append(
                "Review risk factors and consider reducing exposure."
            )

        elif rec == "Sell":

            suggested_action.append(
                "Monitor upcoming news closely and consider "
                "exiting or hedging position."
            )

        elif rec == "Insufficient Data":

            suggested_action.append(
                "Wait for additional market information before "
                "drawing conclusions."
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