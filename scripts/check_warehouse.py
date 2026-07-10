import sqlite3
from pathlib import Path

DB_PATH = Path("data/warehouse/analytics.db")

print("=" * 50)
print("Warehouse Inspection")
print("=" * 50)

print(f"\nDatabase: {DB_PATH.resolve()}")

if not DB_PATH.exists():
    print("\n❌ Database not found.")
    exit()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name;
""")

tables = cursor.fetchall()

print(f"\nFound {len(tables)} tables:\n")

for table in tables:
    table_name = table[0]

    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    rows = cursor.fetchone()[0]

    print(f"{table_name:<30} {rows} rows")

conn.close()

print("\nDone.")