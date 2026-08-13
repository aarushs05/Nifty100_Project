import sqlite3

DB = "data/nifty100.db"

conn = sqlite3.connect(DB)

print("=" * 70)
print("FINANCIAL RATIO CHECK")
print("=" * 70)

for company in ["ATGL", "SBIN"]:

    print(f"\n{company} financial ratios:")

    rows = conn.execute(
        """
        SELECT company_id, year
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year
        """,
        (company,),
    ).fetchall()

    print(rows)
    print("Count:", len(rows))

print("\n" + "=" * 70)
print("SOURCE DATA")
print("=" * 70)

for company in ["ATGL", "SBIN"]:

    print(f"\n{company}")

    for table in [
        "profitandloss",
        "balancesheet",
        "cashflow",
    ]:

        row = conn.execute(
            f"""
            SELECT
                MIN(year),
                MAX(year),
                COUNT(*)
            FROM {table}
            WHERE company_id = ?
            """,
            (company,),
        ).fetchone()

        print(
            f"{table}: "
            f"min={row[0]}, "
            f"max={row[1]}, "
            f"count={row[2]}"
        )

conn.close()