# InsightPulse System Architecture

# InsightPulse System Architecture

```
                              AlphaLens
                    (Data Collection Layer)
     -------------------------------------------------
      NewsAPI | FinBERT | SQLite | Signals | Prices
                         |
                         |
                         ▼
==============================================================
                  InsightPulse
==============================================================

                1. Data Engineering Layer
--------------------------------------------------------------
• Read market.db
• Validate Data
• Data Quality Checks
• Transform & Normalize Data
• Create Analytics Dataset

                         │
                         ▼

                2. Analytics Layer
--------------------------------------------------------------
• News Coverage Analytics
• Sentiment Analytics
• Signal Analytics
• Price Analytics
• Market Attention Analytics
• Trend Analytics
• Correlation Analysis
• Lead-Lag Analysis

                         │
                         ▼

                3. KPI Engine
--------------------------------------------------------------
• News Dominance Index
• Market Mood Index
• Opportunity Score
• Risk Score
• Sentiment Momentum
• Attention Momentum
• Coverage Volatility
• Bullishness Score
• Bearishness Score
• Signal Strength Score
• Signal Stability Index
• Signal Persistence Score
• Price Impact Score
• Attention Shift Score

                         │
                         ▼

            4. Decision Intelligence Engine
--------------------------------------------------------------
• Opportunity Detection
• Risk Detection
• Market Attention Ranking
• Executive Prioritization
• Analyst Recommendation Engine
• Explainability Layer
• Confidence Layer

                         │
                         ▼

                5. Automation Engine
--------------------------------------------------------------
• Daily Market Brief
• Executive Summary
• Automated Insight Feed
• Opportunity Alerts
• Risk Alerts
• Analyst Priority List

                         │
                         ▼

            6. Executive Dashboard (Power BI)
--------------------------------------------------------------
• Executive Overview
• Market Attention
• Sentiment Intelligence
• Opportunity Intelligence
• Risk Intelligence
• Signal Intelligence
• Price Intelligence
• Executive Insights
```
