from core.logger import logger

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

    print("\n2. Available tables...")
    print(list_tables())

    print("\n3. Row counts...")
    print(get_row_counts())

    print("\n4. Schema...")
    print(get_schema())

    print("\n5. Source profile...")
    print(build_source_profile())

    logger.info("-" * 60)
    logger.info("Bootstrap completed successfully.")
    logger.info("-" * 60)


if __name__ == "__main__":
    main()