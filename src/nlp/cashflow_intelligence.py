import sqlite3

import pandas as pd

# --------------------------------------------------
# Load Data
# --------------------------------------------------

conn = sqlite3.connect("data/nifty100.db")

cashflow_df = pd.read_sql("SELECT * FROM cashflow", conn)

ratios_df = pd.read_sql("SELECT * FROM financial_ratios", conn)

# --------------------------------------------------
# Latest Row Per Company
# --------------------------------------------------

latest_cashflow = cashflow_df.sort_values("year").groupby("company_id").tail(1)

latest_ratios = ratios_df.sort_values("year").groupby("company_id").tail(1)

# --------------------------------------------------
# Merge Data
# --------------------------------------------------

merged_df = pd.merge(latest_cashflow, latest_ratios, on="company_id", how="inner")

print(f"Companies found: {len(merged_df)}")

# --------------------------------------------------
# Cash Flow Intelligence Engine
# --------------------------------------------------

results = []

for _, row in merged_df.iterrows():

    company_id = row["company_id"]

    comments = []

    score = 50

    # ----------------------------------------------
    # Operating Cash Flow
    # ----------------------------------------------

    operating_cf = row.get("operating_activity")

    if pd.notna(operating_cf):

        if operating_cf > 0:
            comments.append("Operating cash flow remains positive.")
            score += 20

        elif operating_cf < 0:
            comments.append("Negative operating cash flow is a warning sign.")
            score -= 20

    # ----------------------------------------------
    # FCF Conversion
    # ----------------------------------------------

    fcf_conversion = row.get("fcf_conversion_pct")

    if pd.notna(fcf_conversion):

        if fcf_conversion > 80:
            comments.append("Business converts profits into cash efficiently.")
            score += 15

        elif fcf_conversion < 50:
            comments.append("Weak cash conversion may impact future growth.")
            score -= 15

    # ----------------------------------------------
    # CFO Quality
    # ----------------------------------------------

    cfo_quality = row.get("cfo_quality_score")

    if pd.notna(cfo_quality):

        if cfo_quality > 70:
            comments.append("Cash flow quality appears healthy.")
            score += 15

        elif cfo_quality < 40:
            comments.append(
                "Reported earnings may not be strongly supported by cash generation."
            )
            score -= 15

    # ----------------------------------------------
    # Clamp Score
    # ----------------------------------------------

    score = max(0, min(100, score))

    # ----------------------------------------------
    # Risk Level
    # ----------------------------------------------

    if score >= 75:
        risk_level = "LOW"

    elif score >= 50:
        risk_level = "MEDIUM"

    else:
        risk_level = "HIGH"

    # ----------------------------------------------
    # Health Category
    # ----------------------------------------------

    if score >= 80:
        health = "Excellent"

    elif score >= 65:
        health = "Strong"

    elif score >= 50:
        health = "Average"

    elif score >= 35:
        health = "Weak"

    else:
        health = "Poor"

    # ----------------------------------------------
    # Save Result
    # ----------------------------------------------

    results.append(
        {
            "company_id": company_id,
            "cashflow_health": health,
            "cashflow_comment": " ".join(comments),
            "risk_level": risk_level,
            "cashflow_score": score,
        }
    )

# --------------------------------------------------
# Output
# --------------------------------------------------

cashflow_insights_df = pd.DataFrame(results)

cashflow_insights_df.to_csv("output/cashflow_insights.csv", index=False)

print(f"Companies processed: {len(cashflow_insights_df)}")

print("Output saved: output/cashflow_insights.csv")

print("\nSample Output:\n")

print(cashflow_insights_df.head(10))
