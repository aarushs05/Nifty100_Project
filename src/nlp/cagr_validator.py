import sqlite3

import pandas as pd

# --------------------------------------------------
# Load Data
# --------------------------------------------------

conn = sqlite3.connect("data/nifty100.db")

parsed_df = pd.read_csv("output/analysis_parsed.csv")

ratios_df = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn,
)

# --------------------------------------------------
# Latest Ratio Row Per Company
# --------------------------------------------------

latest_ratios = ratios_df.sort_values("year").groupby("company_id").tail(1)

# --------------------------------------------------
# Mapping
# --------------------------------------------------

sales_map = {3: "revenue_cagr_3yr", 5: "revenue_cagr_5yr", 10: "revenue_cagr_10yr"}

profit_map = {3: "pat_cagr_3yr", 5: "pat_cagr_5yr", 10: "pat_cagr_10yr"}

review_rows = []

# --------------------------------------------------
# Validation Loop
# --------------------------------------------------

for _, row in parsed_df.iterrows():

    company_id = row["company_id"]
    metric_type = row["metric_type"]
    period_years = row["period_years"]
    parsed_pct = row["value_pct"]

    if metric_type not in ["compounded_sales_growth", "compounded_profit_growth"]:
        continue

    ratio_row = latest_ratios[latest_ratios["company_id"] == company_id]

    if ratio_row.empty:
        continue

    if metric_type == "compounded_sales_growth":
        column_name = sales_map.get(period_years)

    else:
        column_name = profit_map.get(period_years)

    if column_name is None:
        continue

    computed_pct = ratio_row.iloc[0][column_name]

    if pd.isna(computed_pct):
        continue

    difference_pct = abs(parsed_pct - computed_pct)

    review_flag = "YES" if difference_pct > 5 else "NO"

    review_rows.append(
        {
            "company_id": company_id,
            "metric_type": metric_type,
            "period_years": period_years,
            "parsed_pct": parsed_pct,
            "computed_pct": round(computed_pct, 2),
            "difference_pct": round(difference_pct, 2),
            "review_flag": review_flag,
        }
    )

# --------------------------------------------------
# Save Output
# --------------------------------------------------

review_df = pd.DataFrame(review_rows)

review_df.to_csv("output/cagr_review.csv", index=False)

print("Review rows :", len(review_df))

print("Flagged rows :", (review_df["review_flag"] == "YES").sum())
