import sqlite3

DB = "data/nifty100.db"

conn = sqlite3.connect(DB)

rows = conn.execute(
    """
    SELECT
        c.id,
        c.company_name,
        COUNT(fr.company_id) AS ratio_count,
        MIN(fr.year) AS first_year,
        MAX(fr.year) AS last_year
    FROM companies c
    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id
    GROUP BY c.id, c.company_name
    ORDER BY ratio_count, c.id
    """
).fetchall()

print("=" * 90)
print("FINANCIAL RATIO COVERAGE")
print("=" * 90)

for row in rows:
    print(row)

print("\nCompanies:", len(rows))
print(
    "Total financial ratio rows:",
    sum(row[2] for row in rows)
)

print("\nCompanies with zero ratio rows:")

for row in rows:
    if row[2] == 0:
        print(row)

print("\nCompanies with fewer than 10 ratio rows:")

for row in rows:
    if row[2] < 10:
        print(row)

conn.close()