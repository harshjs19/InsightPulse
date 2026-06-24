from pprint import pprint

from core.source_manager import (
    validate_source,
    list_tables,
    get_schema,
    get_row_counts,
    build_source_profile,
)


def main():
    print("\n" + "=" * 70)
    print(" InsightPulse Bootstrap")
    print("=" * 70)

    print("\n1. Validating source...")
    pprint(validate_source())

    print("\n2. Available tables...")
    pprint(list_tables())

    print("\n3. Row counts...")
    pprint(get_row_counts())

    print("\n4. Schema...")
    pprint(get_schema())

    print("\n5. Source profile...")
    pprint(build_source_profile())

    print("\n" + "=" * 70)
    print(" Bootstrap completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()