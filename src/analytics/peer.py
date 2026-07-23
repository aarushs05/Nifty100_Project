# """
# Sprint 3 - Peer Comparison Engine

# Outputs:
# 1. output/peer_percentiles.xlsx
# 2. SQLite table: peer_percentiles
# """

# import sqlite3
# from pathlib import Path

# import pandas as pd

# DB = "data/nifty100.db"

# OUTPUT = Path("output")
# OUTPUT.mkdir(exist_ok=True)


# def load_peer_data():
#     """Load all companies with sector information."""

#     conn = sqlite3.connect(DB)

#     query = """
#     SELECT

#         fr.company_id,
#         c.company_name,
#         s.broad_sector,
#         s.sub_sector,
#         fr.year,

#         fr.return_on_equity_pct,
#         fr.return_on_capital_employed_pct,
#         fr.net_profit_margin_pct,
#         fr.debt_to_equity,
#         fr.composite_quality_score,

#         fr.revenue_cagr_3yr,
#         fr.pat_cagr_3yr,
#         fr.eps_cagr_3yr

#     FROM financial_ratios fr

#     JOIN sectors s
#         ON fr.company_id = s.company_id

#     JOIN companies c
#         ON fr.company_id = c.id
#     """

#     df = pd.read_sql(query, conn)

#     conn.close()

#     return df


# def calculate_percentiles(df):
#     """Calculate sector-wise percentile ranks."""

#     metrics = [

#         "return_on_equity_pct",

#         "return_on_capital_employed_pct",

#         "net_profit_margin_pct",

#         "composite_quality_score",

#         "revenue_cagr_3yr",

#         "pat_cagr_3yr",

#         "eps_cagr_3yr",

#     ]

#     result = df.copy()

#     for metric in metrics:

#         result[f"{metric}_percentile"] = (

#             result
#             .groupby("broad_sector")[metric]
#             .rank(method="average", pct=True)

#             * 100

#         ).round(2)

#     return result


# def save_to_database(df):
#     """Store percentile table inside SQLite."""

#     conn = sqlite3.connect(DB)

#     df.to_sql(
#         "peer_percentiles",
#         conn,
#         if_exists="replace",
#         index=False,
#     )

#     conn.close()

#     print("\n✓ peer_percentiles table created successfully.")


# def export_excel(df):
#     """Export Excel report."""

#     output_file = OUTPUT / "peer_percentiles.xlsx"

#     df.to_excel(
#         output_file,
#         index=False,
#     )

#     print(f"\n✓ Excel exported -> {output_file}")


# def main():

#     print("\nLoading Peer Data...")

#     df = load_peer_data()

#     print(f"Loaded {len(df)} rows")

#     print("\nCalculating Percentiles...")

#     ranked = calculate_percentiles(df)

#     export_excel(ranked)

#     save_to_database(ranked)

#     print("\nPreview:\n")

#     print(

#         ranked[
#             [

#                 "company_id",

#                 "broad_sector",

#                 "return_on_equity_pct",

#                 "return_on_equity_pct_percentile",

#                 "return_on_capital_employed_pct",

#                 "return_on_capital_employed_pct_percentile",

#                 "composite_quality_score",

#                 "composite_quality_score_percentile",

#             ]

#         ].head(10)

#     )


# if __name__ == "__main__":
#     main()


import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

print(
    pd.read_sql(
        "SELECT COUNT(*) FROM peer_percentiles",
        conn,
    )
)

conn.close()