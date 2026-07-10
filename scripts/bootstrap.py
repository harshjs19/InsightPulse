import sqlite3
from config.settings import ANALYTICS_DB
from core.logger import logger

from core.snapshot_manager import create_snapshot
from core.warehouse_manager import initialize_warehouse
from etl.extract import extract_all
from etl.transform import transform_all
from etl.load import load_all
from analytics.company_metrics import build_company_metrics
from analytics.company_intelligence import build_company_intelligence
from analytics.explanations import build_explanations
from analytics.build_insights import build_insights
from etl.save_company_intelligence import (
    save_company_intelligence
)

from analytics.market_insights import (
    generate_market_insights
)

from etl.save_market_insights import (
    save_market_insights
)

from core.source_manager import (
    validate_source,
    list_tables,
    get_schema,
    get_row_counts,
    build_source_profile,
)


def main():
    logger.info("-" * 60)
    logger.info("InsightPulse Bootstrap")
    logger.info("-" * 60)

    print("\n1. Validating source...")
    print(validate_source())

    print("\n2. Creating snapshot...")
    snapshot = create_snapshot()
    print(f"Snapshot: {snapshot}")

    print("\n3. Initializing warehouse...")
    warehouse = initialize_warehouse()
    print(f"Warehouse: {warehouse}")

    print("\n4. Available tables...")
    print(list_tables())

    print("\n5. Row counts...")
    print(get_row_counts())

    print("\n6. Schema...")
    print(get_schema())

    print("\n7. Source profile...")
    print(build_source_profile())

    print("\n8. Extracting data...")
    tables = extract_all()

    for name, dataframe in tables.items():
        print(f"{name}: {len(dataframe)} rows")

    print("\n9. Transforming data...")
    transformed_tables = transform_all(tables)

    for name, dataframe in transformed_tables.items():
        print(f"{name}: {len(dataframe)} rows")

    print("\n10. Loading data into warehouse...")
    load_all(transformed_tables)
    print("Analytics warehouse updated successfully.")

    print("\n11. Building company metrics...")

    company_metrics = build_company_metrics(
        transformed_tables
    )

    with sqlite3.connect(ANALYTICS_DB) as conn:
        company_metrics.to_sql(
        "company_metrics",
        conn,
        if_exists="replace",
        index=False
    )

    print(
        f"Generated metrics for {len(company_metrics)} companies."
    )

    print("\n12. Building company intelligence...")
    intelligence = build_company_intelligence(
        company_metrics
    )

    print("\n13. Building insights...")
    intelligence = build_insights(intelligence)

    print("\n14. Building explanations...")
    intelligence = build_explanations(intelligence)

    print("\n15. Saving company intelligence...")
    save_company_intelligence(intelligence)

    print("\n16. Generating market insights...")
    insights = generate_market_insights(intelligence)
    save_market_insights(insights)

    print("\n17. Market Insights...\n")

    print("Executive Brief")
    print("-" * 60)

    print(
        insights["executive_brief"].iloc[0]
    )

    print(
        f"\nGenerated intelligence for {len(intelligence)} companies."
    )


# pyrefly: ignore [parse-error]
if __name__ == "__main__":
    main()