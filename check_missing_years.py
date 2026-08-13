import sqlite3
import pandas as pd

DB = "data/nifty100.db"

conn = sqlite3.connect(DB)

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
]

print("=" * 80)
print("RATIO ENGINE YEAR-COVERAGE DIAGNOSTIC")
print("=" * 80)

# Get all companies
companies = pd.read_sql(
    """
    SELECT id, company_name
    FROM companies
    ORDER BY id
    """,
    conn,
)

print(f"\nCompanies: {len(companies)}")

for company_id in companies["id"]:

    print("\n" + "-" * 80)
    print(company_id)

    for table in tables:

        df = pd.read_sql(
            f"""
            SELECT year
            FROM {table}
            WHERE company_id = ?
            ORDER BY year
            """,
            conn,
            params=(company_id,),
        )

        years = sorted(
            pd.to_numeric(
                df["year"],
                errors="coerce"
            )
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )

        print(
            f"{table:15s}: "
            f"{len(years):2d} rows | "
            f"{years}"
        )

    # Years common to all three tables
    year_sets = []

    for table in tables:

        df = pd.read_sql(
            f"""
            SELECT year
            FROM {table}
            WHERE company_id = ?
            """,
            conn,
            params=(company_id,),
        )

        years = set(
            pd.to_numeric(
                df["year"],
                errors="coerce"
            )
            .dropna()
            .astype(int)
            .tolist()
        )

        year_sets.append(years)

    common = sorted(
        year_sets[0]
        & year_sets[1]
        & year_sets[2]
    )

    print(
        f"{'COMMON YEARS':15s}: "
        f"{len(common):2d} rows | "
        f"{common}"
    )

print("\n" + "=" * 80)
print("ATGL / SBIN DETAILED CHECK")
print("=" * 80)

for company_id in ["ATGL", "SBIN"]:

    print(f"\n### {company_id}")

    for table in tables:

        df = pd.read_sql(
            f"""
            SELECT *
            FROM {table}
            WHERE company_id = ?
            ORDER BY year
            """,
            conn,
            params=(company_id,),
        )

        print(f"\n{table}:")
        print(df.to_string(index=False))

conn.close()