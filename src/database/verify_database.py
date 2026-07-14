import sqlite3

DB_PATH = "data/nifty100.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("=" * 60)
print("DATABASE VERIFICATION")
print("=" * 60)

for table in tables:
    table_name = table[0]

    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]

    print(f"{table_name:<20} {count:>6} rows")

conn.close()

print("\nVerification Complete!")