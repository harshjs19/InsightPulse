# InsightPulse Analytics Warehouse

## Philosophy

InsightPulse will **not** query AlphaLens tables directly.

Instead, AlphaLens acts as the **Operational Database (OLTP)**, while InsightPulse maintains its own **Analytics Warehouse (OLAP)**.

This separation keeps the analytics platform independent, scalable, and optimized for reporting.

---

# Data Flow

```text
AlphaLens (market.db)
        │
        ▼
ETL / Data Transformation
        │
        ▼
InsightPulse Analytics Warehouse
        │
        ▼
Power BI
```

---

# Warehouse Layers

## Layer 1 — Source Layer

Purpose:

Store raw operational data from AlphaLens.

Tables:

* news
* sentiment
* prices

These tables are **read-only** inside InsightPulse.

---

## Layer 2 — Analytics Layer

Purpose:

Clean, enrich, validate and transform raw data.

This layer prepares data for reporting.

Examples:

* Daily sentiment
* Company level summaries
* Price change calculations
* Coverage statistics
* Momentum calculations

---

## Layer 3 — Business Layer

Purpose:

Generate reusable business metrics.

Examples:

* Opportunity Score
* Risk Score
* Market Mood Index
* Attention Score
* Coverage Index
* Signal Strength
* Confidence Score

No dashboard should calculate these independently.

Every report uses the same business definitions.

---

## Layer 4 — Decision Intelligence Layer

Purpose:

Generate business insights rather than charts.

Examples:

* Companies requiring attention
* Emerging opportunities
* Emerging risks
* Executive recommendations
* Daily market summary
* Analyst priority list

---

## Layer 5 — Presentation Layer

Power BI becomes the presentation layer only.

It consumes prepared analytical data.

Business logic should remain inside the warehouse whenever possible.

---

# Design Principles

* Separate operational and analytical databases.
* Never modify AlphaLens source tables.
* Create reusable business metrics.
* Keep Power BI lightweight.
* Every insight must be explainable.
* Every KPI should have a single source of truth.
* Build for scalability rather than today's dataset.
