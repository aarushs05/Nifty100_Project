import sqlite3

conn = sqlite3.connect("data/nifty100.db")
cursor = conn.cursor()

tables = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
).fetchall()

for (table,) in tables:
    print("\n" + "=" * 60)
    print(table)
    print("=" * 60)

    cursor.execute(f"PRAGMA table_info({table})")

    for row in cursor.fetchall():
        print(row)

conn.close()