import sqlite3

import pandas as pd

# --------------------------------------------------
# Load Data
# --------------------------------------------------

conn = sqlite3.connect("data/nifty100.db")

ratios_df = pd.read_sql("SELECT * FROM financial_ratios", conn)

latest_ratios = ratios_df.sort_values("year").groupby("company_id").tail(1)

print(f"Companies found: {len(latest_ratios)}")

# --------------------------------------------------
# Capital Allocation Engine
# --------------------------------------------------

results = []

for _, row in latest_ratios.iterrows():

    company_id = row["company_id"]

    comments = []

    score = 50

    roe = row.get("return_on_equity_pct")
    roce = row.get("return_on_capital_employed_pct")
    debt = row.get("debt_to_equity")
    capex = row.get("capex_intensity_pct")

    # ----------------------------------------------
    # ROE
    # ----------------------------------------------

    if pd.notna(roe):

        if roe > 20:
            comments.append("Strong shareholder returns.")
            score += 15

        elif roe < 10:
            comments.append("Low shareholder returns.")
            score -= 15

    # ----------------------------------------------
    # ROCE
    # ----------------------------------------------

    if pd.notna(roce):

        if roce > 20:
            comments.append("Capital employed efficiently.")
            score += 15

        elif roce < 10:
            comments.append("Weak capital efficiency.")
            score -= 15

    # ----------------------------------------------
    # Debt
    # ----------------------------------------------

    if pd.notna(debt):

        if debt < 0.5:
            comments.append("Balance sheet remains conservative.")
            score += 10

        elif debt > 1:
            comments.append("High leverage may reduce flexibility.")
            score -= 10

    # ----------------------------------------------
    # Capex
    # ----------------------------------------------

    if pd.notna(capex):

        if capex < 10:
            comments.append("Business requires modest capital investment.")
            score += 10

        elif capex > 25:
            comments.append("Business requires significant capital investment.")
            score -= 10

    # ----------------------------------------------
    # Clamp Score
    # ----------------------------------------------

    score = max(0, min(100, score))

    # ----------------------------------------------
    # Rating
    # ----------------------------------------------

    if score >= 80:
        quality = "Excellent"

    elif score >= 65:
        quality = "Strong"

    elif score >= 50:
        quality = "Average"

    elif score >= 35:
        quality = "Weak"

    else:
        quality = "Poor"

    # ----------------------------------------------
    # Save
    # ----------------------------------------------

    results.append(
        {
            "company_id": company_id,
            "allocation_quality": quality,
            "allocation_comment": " ".join(comments),
            "allocation_score": score,
        }
    )

# --------------------------------------------------
# Output
# --------------------------------------------------

allocation_df = pd.DataFrame(results)

allocation_df.to_csv("output/capital_allocation_insights.csv", index=False)

print(f"Companies processed: {len(allocation_df)}")

print("Output saved: output/capital_allocation_insights.csv")

print("\nSample Output:\n")

print(allocation_df.head(10))
