import numpy as np
import pandas as pd


# =============================================================================
# Scoring Constants
# =============================================================================

# --- Confidence Score Weights ---
# Three-factor model: sample adequacy, model certainty, sentiment agreement.
# Sample adequacy (0.40): Statistical power — larger samples produce more
#     reliable estimates. The most fundamental constraint.
# Model certainty (0.35): FinBERT's probability output — the most direct,
#     granular measure of prediction quality.
# Sentiment agreement (0.25): When articles strongly disagree, the aggregate
#     sentiment mean is unreliable (analyst dispersion effect).

WEIGHT_SAMPLE_ADEQUACY = 0.40
WEIGHT_MODEL_CERTAINTY = 0.35
WEIGHT_SENTIMENT_AGREEMENT = 0.25

# Sample saturation point: CLT convergence — after ~20 independent
# observations, the sample mean stabilizes. Diminishing returns beyond this.
SAMPLE_SATURATION_POINT = 20

# --- Momentum Index Weights ---
# Momentum is fundamentally about direction (sentiment), amplified by
# visibility (attention). Academic momentum literature (Jegadeesh & Titman
# 1993) finds the return signal dominates volume by ~2:1 to 3:1.

WEIGHT_MOMENTUM_SENTIMENT = 0.70
WEIGHT_MOMENTUM_ATTENTION = 0.30

# --- Risk Score Weights ---
# Two-factor model: negative sentiment and uncertainty.
# Negative sentiment (0.65): The most direct risk indicator — bad news
#     predicts bad outcomes. Analogous to CDS spread widening.
# Uncertainty (0.35): Low confidence means we cannot rule out adverse
#     outcomes. In finance, uncertainty commands a risk premium
#     (Pástor & Veronesi 2003).

WEIGHT_NEGATIVE_SENTIMENT = 0.65
WEIGHT_UNCERTAINTY = 0.35

# --- Opportunity Score Weights ---
# Three-factor model: sentiment signal, momentum confirmation, signal
# reliability.
# Sentiment (0.50): The primary opportunity signal — strongest predictor
#     of upside potential.
# Momentum (0.25): Trend confirmation — validates that sentiment has
#     directional persistence.
# Confidence (0.25): Signal quality gate — prevents surfacing spurious
#     opportunities from thin data.

WEIGHT_OPPORTUNITY_SENTIMENT = 0.50
WEIGHT_OPPORTUNITY_MOMENTUM = 0.25
WEIGHT_OPPORTUNITY_CONFIDENCE = 0.25

# --- Attention Score Thresholds ---
ATTENTION_VERY_HIGH = 75
ATTENTION_HIGH = 50
ATTENTION_MEDIUM = 25

# --- Sentiment Score Thresholds ---
SENTIMENT_VERY_POSITIVE = 70
SENTIMENT_POSITIVE = 55
SENTIMENT_NEUTRAL = 45
SENTIMENT_NEGATIVE = 30

# --- Momentum Index Thresholds ---
MOMENTUM_STRONG = 75
MOMENTUM_MODERATE = 55
MOMENTUM_WEAK = 35

# --- Confidence Score Thresholds ---
CONFIDENCE_VERY_HIGH = 80
CONFIDENCE_HIGH = 60
CONFIDENCE_MEDIUM = 40
CONFIDENCE_LOW = 25

# --- Risk Score Thresholds ---
RISK_HIGH = 75
RISK_MODERATE = 55
RISK_LOW = 35

# --- Opportunity Score Thresholds ---
OPPORTUNITY_HIGH = 75
OPPORTUNITY_MODERATE = 55
OPPORTUNITY_LOW = 35

# --- Recommendation Thresholds ---
# Net score = opportunity_score - risk_score. This single axis captures
# the essential question: "does opportunity outweigh risk?" Thresholds
# are calibrated to the actual score distribution produced by FinBERT
# sentiment data, where most companies cluster near neutral.

REC_STRONG_BUY_NET = 25
REC_STRONG_BUY_CONFIDENCE = 60

REC_BUY_NET = 10
REC_BUY_CONFIDENCE = 50

REC_ACCUMULATE_NET = 0
REC_ACCUMULATE_CONFIDENCE = 40

REC_HOLD_NET = -10

REC_REDUCE_CONFIDENCE = 30

REC_SELL_NET = -25
REC_SELL_CONFIDENCE = 60

REC_INSUFFICIENT_DATA_CONFIDENCE = 30


# =============================================================================
# Company Intelligence Engine
# =============================================================================


def build_company_intelligence(company_metrics: pd.DataFrame) -> pd.DataFrame:
    intelligence = company_metrics.copy()

    # -------------------------
    # Attention Score
    # -------------------------

    max_news = intelligence["total_news"].max()

    if max_news == 0:
        intelligence["attention_score"] = 0
    else:
        intelligence["attention_score"] = (
            intelligence["total_news"] / max_news
        ) * 100

    intelligence["attention_score"] = (
        intelligence["attention_score"]
        .clip(0, 100)
        .round(1)
    )

    attention_conditions = [
        intelligence["attention_score"] >= ATTENTION_VERY_HIGH,
        intelligence["attention_score"] >= ATTENTION_HIGH,
        intelligence["attention_score"] >= ATTENTION_MEDIUM,
    ]

    attention_labels = [
        "Very High",
        "High",
        "Medium",
    ]

    intelligence["attention_level"] = np.select(
        attention_conditions,
        attention_labels,
        default="Low",
    )

    # -------------------------
    # Sentiment Score
    # -------------------------

    intelligence["sentiment_score"] = (
        (intelligence["avg_sentiment"] + 1) / 2
    ) * 100

    intelligence["sentiment_score"] = (
        intelligence["sentiment_score"]
        .clip(0, 100)
        .round(1)
    )

    sentiment_conditions = [
        intelligence["sentiment_score"] >= SENTIMENT_VERY_POSITIVE,
        intelligence["sentiment_score"] >= SENTIMENT_POSITIVE,
        intelligence["sentiment_score"] >= SENTIMENT_NEUTRAL,
        intelligence["sentiment_score"] >= SENTIMENT_NEGATIVE,
    ]

    sentiment_labels = [
        "Very Positive",
        "Positive",
        "Neutral",
        "Negative",
    ]

    intelligence["sentiment_level"] = np.select(
        sentiment_conditions,
        sentiment_labels,
        default="Very Negative",
    )

    # -------------------------
    # Confidence Score
    # -------------------------
    # Three-factor model:
    #   1. Sample adequacy  — do we have enough articles?
    #   2. Model certainty  — how sure is FinBERT about its classifications?
    #   3. Sentiment agreement — do the articles agree on direction?

    # Factor 1: Sample adequacy (saturating curve, diminishing returns)
    sample_adequacy = (
        intelligence["total_news"]
        .clip(upper=SAMPLE_SATURATION_POINT)
        / SAMPLE_SATURATION_POINT
    ) * 100

    # Factor 2: Model certainty (FinBERT probability, already 0–1)
    model_certainty = intelligence["avg_confidence"] * 100

    # Factor 3: Sentiment agreement (1 − dispersion)
    # Dispersion = fraction of articles that are polarized (positive OR
    # negative). High dispersion = disagreement = low agreement.
    sentiment_dispersion = (
        (intelligence["positive_news"] + intelligence["negative_news"])
        / intelligence["total_news"].clip(lower=1)
    )

    sentiment_agreement = (1 - sentiment_dispersion) * 100

    intelligence["confidence_score"] = (
        sample_adequacy * WEIGHT_SAMPLE_ADEQUACY +
        model_certainty * WEIGHT_MODEL_CERTAINTY +
        sentiment_agreement * WEIGHT_SENTIMENT_AGREEMENT
    )

    intelligence["confidence_score"] = (
        intelligence["confidence_score"]
        .clip(0, 100)
        .round(1)
    )

    confidence_conditions = [
        intelligence["confidence_score"] >= CONFIDENCE_VERY_HIGH,
        intelligence["confidence_score"] >= CONFIDENCE_HIGH,
        intelligence["confidence_score"] >= CONFIDENCE_MEDIUM,
        intelligence["confidence_score"] >= CONFIDENCE_LOW,
    ]

    confidence_labels = [
        "Very High",
        "High",
        "Medium",
        "Low",
    ]

    intelligence["confidence_level"] = np.select(
        confidence_conditions,
        confidence_labels,
        default="Very Low",
    )

    # -------------------------
    # Momentum Index
    # -------------------------
    # Momentum = direction (sentiment) amplified by visibility (attention).
    # Sentiment dominates because momentum is fundamentally directional.

    intelligence["momentum_index"] = (
        intelligence["sentiment_score"] * WEIGHT_MOMENTUM_SENTIMENT +
        intelligence["attention_score"] * WEIGHT_MOMENTUM_ATTENTION
    )

    intelligence["momentum_index"] = (
        intelligence["momentum_index"]
        .clip(0, 100)
        .round(1)
    )

    momentum_conditions = [
        intelligence["momentum_index"] >= MOMENTUM_STRONG,
        intelligence["momentum_index"] >= MOMENTUM_MODERATE,
        intelligence["momentum_index"] >= MOMENTUM_WEAK,
    ]

    momentum_labels = [
        "Strong",
        "Moderate",
        "Weak",
    ]

    intelligence["momentum_level"] = np.select(
        momentum_conditions,
        momentum_labels,
        default="Very Weak",
    )

    # -------------------------
    # Risk Score
    # -------------------------
    # Two-factor model:
    #   1. Negative sentiment — bad news predicts bad outcomes.
    #   2. Uncertainty — low confidence means we cannot rule out
    #      adverse outcomes.

    negative_sentiment_risk = 100 - intelligence["sentiment_score"]

    uncertainty_penalty = 100 - intelligence["confidence_score"]

    intelligence["risk_score"] = (
        negative_sentiment_risk * WEIGHT_NEGATIVE_SENTIMENT +
        uncertainty_penalty * WEIGHT_UNCERTAINTY
    )

    intelligence["risk_score"] = (
        intelligence["risk_score"]
        .clip(0, 100)
        .round(1)
    )

    risk_conditions = [
        intelligence["risk_score"] >= RISK_HIGH,
        intelligence["risk_score"] >= RISK_MODERATE,
        intelligence["risk_score"] >= RISK_LOW,
    ]

    risk_levels = [
        "High",
        "Moderate",
        "Low",
    ]

    intelligence["risk_level"] = np.select(
        risk_conditions,
        risk_levels,
        default="Very Low",
    )

    # -------------------------
    # Opportunity Score
    # -------------------------
    # Three-factor model:
    #   1. Sentiment — the primary opportunity signal.
    #   2. Momentum — trend confirmation (directional persistence).
    #   3. Confidence — signal quality gate.

    intelligence["opportunity_score"] = (
        intelligence["sentiment_score"] * WEIGHT_OPPORTUNITY_SENTIMENT +
        intelligence["momentum_index"] * WEIGHT_OPPORTUNITY_MOMENTUM +
        intelligence["confidence_score"] * WEIGHT_OPPORTUNITY_CONFIDENCE
    )

    intelligence["opportunity_score"] = (
        intelligence["opportunity_score"]
        .clip(0, 100)
        .round(1)
    )

    opportunity_conditions = [
        intelligence["opportunity_score"] >= OPPORTUNITY_HIGH,
        intelligence["opportunity_score"] >= OPPORTUNITY_MODERATE,
        intelligence["opportunity_score"] >= OPPORTUNITY_LOW,
    ]

    opportunity_levels = [
        "High",
        "Moderate",
        "Low",
    ]

    intelligence["opportunity_level"] = np.select(
        opportunity_conditions,
        opportunity_levels,
        default="Very Low",
    )

    # -------------------------
    # Recommendation Engine
    # -------------------------
    # Net-score decision matrix using sell-side terminology.
    # net_score = opportunity - risk captures the essential question:
    # "does opportunity outweigh risk?" Evaluated top-down.

    net_score = (
        intelligence["opportunity_score"] -
        intelligence["risk_score"]
    )

    conditions = [
        # Insufficient Data: checked first — cannot recommend without evidence
        (
            intelligence["confidence_score"] < REC_INSUFFICIENT_DATA_CONFIDENCE
        ),

        # Strong Buy: high-conviction opportunity dominates risk
        (
            (net_score >= REC_STRONG_BUY_NET) &
            (intelligence["confidence_score"] >= REC_STRONG_BUY_CONFIDENCE)
        ),

        # Buy: clear opportunity edge with reasonable evidence
        (
            (net_score >= REC_BUY_NET) &
            (intelligence["confidence_score"] >= REC_BUY_CONFIDENCE)
        ),

        # Accumulate: slight positive tilt, worth building a position
        (
            (net_score >= REC_ACCUMULATE_NET) &
            (intelligence["confidence_score"] >= REC_ACCUMULATE_CONFIDENCE)
        ),

        # Sell: high-conviction risk dominates opportunity
        (
            (net_score < REC_SELL_NET) &
            (intelligence["confidence_score"] >= REC_SELL_CONFIDENCE)
        ),

        # Reduce: risk clearly dominates with sufficient evidence
        (
            (net_score < REC_HOLD_NET) &
            (intelligence["confidence_score"] >= REC_REDUCE_CONFIDENCE)
        ),
    ]

    recommendations = [
        "Insufficient Data",
        "Strong Buy",
        "Buy",
        "Accumulate",
        "Sell",
        "Reduce",
    ]

    intelligence["recommendation"] = np.select(
        conditions,
        recommendations,
        default="Hold",
    )

    derived_columns = [
        "attention_score",
        "attention_level",
        "sentiment_score",
        "sentiment_level",
        "momentum_index",
        "momentum_level",
        "confidence_score",
        "confidence_level",
        "risk_score",
        "risk_level",
        "opportunity_score",
        "opportunity_level",
        "recommendation",
    ]
    ordered_columns = list(company_metrics.columns) + derived_columns
    remaining_columns = [
        column
        for column in intelligence.columns
        if column not in ordered_columns
    ]

    return intelligence[ordered_columns + remaining_columns]
