import sqlite3

import pandas as pd

# --------------------------------------------------
# Load Data
# --------------------------------------------------

conn = sqlite3.connect("data/nifty100.db")

ratios_df = pd.read_sql("SELECT * FROM financial_ratios", conn)

# --------------------------------------------------
# Latest Ratio Row Per Company
# --------------------------------------------------

latest_ratios = ratios_df.sort_values("year").groupby("company_id").tail(1)

print(f"Companies found: {len(latest_ratios)}")

# --------------------------------------------------
# Pros / Cons Engine
# --------------------------------------------------

results = []

for _, row in latest_ratios.iterrows():

    company_id = row["company_id"]

    pros = []
    cons = []

    # ==================================================
    # PRO RULES
    # ==================================================

    if pd.notna(row["return_on_equity_pct"]) and row["return_on_equity_pct"] > 20:
        pros.append("Strong return on equity")

    if (
        pd.notna(row["return_on_capital_employed_pct"])
        and row["return_on_capital_employed_pct"] > 20
    ):
        pros.append("Efficient capital allocation")

    if pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] < 0.5:
        pros.append("Conservative balance sheet")

    if pd.notna(row["revenue_cagr_5yr"]) and row["revenue_cagr_5yr"] > 15:
        pros.append("Healthy revenue growth")

    if pd.notna(row["pat_cagr_5yr"]) and row["pat_cagr_5yr"] > 15:
        pros.append("Strong profit growth")

    if pd.notna(row["interest_coverage"]) and row["interest_coverage"] > 10:
        pros.append("Strong interest coverage")

    if pd.notna(row["fcf_conversion_pct"]) and row["fcf_conversion_pct"] > 80:
        pros.append("Healthy free cash flow generation")

    if pd.notna(row["cfo_quality_score"]) and row["cfo_quality_score"] > 70:
        pros.append("High earnings quality")

    # ==================================================
    # CON RULES
    # ==================================================

    if pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] > 1:
        cons.append("High leverage levels")

    if pd.notna(row["interest_coverage"]) and row["interest_coverage"] < 3:
        cons.append("Weak interest coverage")

    if pd.notna(row["revenue_cagr_5yr"]) and row["revenue_cagr_5yr"] < 5:
        cons.append("Slow revenue growth")

    if pd.notna(row["return_on_equity_pct"]) and row["return_on_equity_pct"] < 10:
        cons.append("Low shareholder returns")

    if pd.notna(row["pat_cagr_5yr"]) and row["pat_cagr_5yr"] < 5:
        cons.append("Weak profit growth")

    if pd.notna(row["fcf_conversion_pct"]) and row["fcf_conversion_pct"] < 50:
        cons.append("Weak cash conversion")

    if pd.notna(row["cfo_quality_score"]) and row["cfo_quality_score"] < 40:
        cons.append("Low earnings quality")

    if pd.notna(row["capex_intensity_pct"]) and row["capex_intensity_pct"] > 25:
        cons.append("High capital expenditure requirements")

    # ==================================================
    # CONFIDENCE SCORE
    # ==================================================

    trigger_count = len(pros) + len(cons)

    confidence_score = round((trigger_count / 16) * 100, 2)

    # ==================================================
    # STORE RESULT
    # ==================================================

    results.append(
        {
            "company_id": company_id,
            "pros": "; ".join(pros) if pros else "No major strengths identified",
            "cons": "; ".join(cons) if cons else "No major concerns identified",
            "confidence_score": confidence_score,
        }
    )

# --------------------------------------------------
# Save Output
# --------------------------------------------------

pros_cons_df = pd.DataFrame(results)

pros_cons_df.to_csv("output/pros_cons_generated.csv", index=False)

print(f"Companies processed: {len(pros_cons_df)}")

print("Output saved: output/pros_cons_generated.csv")

print("\nSample Output:\n")
print(pros_cons_df.head(10))
