import pandas as pd

# --------------------------------------------------
# Load Data
# --------------------------------------------------

pros_cons = pd.read_csv("output/pros_cons_generated.csv")

cashflow = pd.read_csv("output/cashflow_insights.csv")

allocation = pd.read_csv("output/capital_allocation_insights.csv")

# --------------------------------------------------
# Merge Data
# --------------------------------------------------

merged = pros_cons.merge(cashflow, on="company_id", how="inner").merge(
    allocation, on="company_id", how="inner"
)

print(f"Companies found: {len(merged)}")

# --------------------------------------------------
# Narrative Engine
# --------------------------------------------------

results = []

for _, row in merged.iterrows():

    company = row["company_id"]

    # ----------------------------------------------
    # Weighted Overall Score
    # ----------------------------------------------

    overall_score = round(
        (
            (row["confidence_score"] * 0.20)
            + (row["cashflow_score"] * 0.40)
            + (row["allocation_score"] * 0.40)
        ),
        2,
    )

    # ----------------------------------------------
    # Rating
    # ----------------------------------------------

    if overall_score >= 70:
        rating = "Excellent"

    elif overall_score >= 60:
        rating = "Strong"

    elif overall_score >= 45:
        rating = "Average"

    elif overall_score >= 30:
        rating = "Weak"

    else:
        rating = "Poor"

    # ----------------------------------------------
    # Top Pro
    # ----------------------------------------------

    pros_text = str(row["pros"])

    if (
        pros_text.strip() == ""
        or pros_text == "nan"
        or "No major strengths" in pros_text
    ):
        top_pro = "stable operating profile"

    else:
        top_pro = pros_text.split(";")[0].strip()

    # ----------------------------------------------
    # Top Con
    # ----------------------------------------------

    cons_text = str(row["cons"])

    if (
        cons_text.strip() == ""
        or cons_text == "nan"
        or "No major concerns" in cons_text
    ):
        top_con = "no major concerns identified"

    else:
        top_con = cons_text.split(";")[0].strip()

    # ----------------------------------------------
    # Supporting Comments
    # ----------------------------------------------

    cashflow_comment = str(row["cashflow_comment"])

    allocation_comment = str(row["allocation_comment"])

    # ----------------------------------------------
    # Narrative
    # ----------------------------------------------

    narrative = (
        f"{company} demonstrates {top_pro.lower()}. "
        f"{cashflow_comment} "
        f"{allocation_comment} "
        f"Key concern: {top_con.lower()}. "
        f"Overall rating: {rating}."
    )

    # ----------------------------------------------
    # Save Result
    # ----------------------------------------------

    results.append(
        {
            "company_id": company,
            "overall_rating": rating,
            "overall_score": overall_score,
            "narrative": narrative,
        }
    )

# --------------------------------------------------
# Create Output
# --------------------------------------------------

narratives_df = pd.DataFrame(results)

narratives_df.to_csv("output/company_narratives.csv", index=False)

# --------------------------------------------------
# Summary
# --------------------------------------------------

print(f"Companies processed: {len(narratives_df)}")

print("Output saved: output/company_narratives.csv")

print("\nSample Output:\n")

print(narratives_df.head(10))
