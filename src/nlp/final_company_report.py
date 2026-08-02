import pandas as pd

# --------------------------------------------------
# Load Generated Outputs
# --------------------------------------------------

pros_cons = pd.read_csv(
    "output/pros_cons_generated.csv"
)

cashflow = pd.read_csv(
    "output/cashflow_insights.csv"
)

allocation = pd.read_csv(
    "output/capital_allocation_insights.csv"
)

narratives = pd.read_csv(
    "output/company_narratives.csv"
)

# --------------------------------------------------
# Merge All Outputs
# --------------------------------------------------

final_df = (
    pros_cons
    .merge(
        cashflow,
        on="company_id",
        how="inner"
    )
    .merge(
        allocation,
        on="company_id",
        how="inner"
    )
    .merge(
        narratives,
        on="company_id",
        how="inner"
    )
)

print(f"Companies found: {len(final_df)}")

# --------------------------------------------------
# Select Final Columns
# --------------------------------------------------

final_df = final_df[
    [
        "company_id",

        "overall_rating",
        "overall_score",

        "pros",
        "cons",
        "confidence_score",

        "cashflow_health",
        "cashflow_score",
        "risk_level",

        "allocation_quality",
        "allocation_score",

        "narrative"
    ]
]

# --------------------------------------------------
# Sort by Overall Score
# --------------------------------------------------

final_df = final_df.sort_values(
    by="overall_score",
    ascending=False
)

# --------------------------------------------------
# Reset Index
# --------------------------------------------------

final_df = final_df.reset_index(
    drop=True
)

# --------------------------------------------------
# Save Output
# --------------------------------------------------

final_df.to_csv(
    "output/final_company_report.csv",
    index=False
)

# --------------------------------------------------
# Summary
# --------------------------------------------------

print(
    f"Companies processed: {len(final_df)}"
)

print(
    "Output saved: output/final_company_report.csv"
)

print("\nFinal Dataset Shape:")

print(final_df.shape)

print("\nTop 10 Companies:\n")

print(final_df.head(10))