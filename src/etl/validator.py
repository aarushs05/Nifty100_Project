import pandas as pd

from loader import ExcelLoader
from dq_rules import (
    dq01_primary_key,
    dq02_company_year,
    dq03_foreign_key,
)

# ----------------------------
# Load all datasets
# ----------------------------

loader = ExcelLoader()
datasets = loader.load_all()

failures = []

# ----------------------------
# Dataset Categories
# ----------------------------

PK_DATASETS = {
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx",
}
COMPANY_YEAR_DATASETS = {
    "market_cap.xlsx",
}


FK_DATASETS = {
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "documents.xlsx",
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx",
}

# ----------------------------
# Companies Reference Table
# ----------------------------

companies = datasets["companies.xlsx"]

# ----------------------------
# Execute Validation Rules
# ----------------------------

for name, df in datasets.items():

    # DQ-01 Primary Key
    if name in PK_DATASETS:
        failures.extend(
            dq01_primary_key(df, name)
        )

    # DQ-02 Company + Year
    if name in COMPANY_YEAR_DATASETS:
        failures.extend(
            dq02_company_year(df, name)
        )

    # DQ-03 Foreign Key
    if name in FK_DATASETS:
        failures.extend(
            dq03_foreign_key(
                df,
                companies,
                name
            )
        )

# ----------------------------
# Export Validation Report
# ----------------------------

failure_df = pd.DataFrame(failures)

failure_df.to_csv(
    "output/validation_failures.csv",
    index=False
)
# ----------------------------
# Print Summary
# ----------------------------

print("=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)

print(f"Datasets Checked : {len(datasets)}")
print(f"Total Failures   : {len(failure_df)}")

if failure_df.empty:
    print("\n✅ No validation failures found.")
else:
    print("\nFailure Count by Rule")
    print(failure_df.groupby("rule").size())

    print("\nFailure Count by Dataset")
    print(failure_df.groupby("dataset").size())

    print("\nTop 10 Failures")
    print(failure_df.head(10))




# from loader import ExcelLoader

# loader = ExcelLoader()
# datasets = loader.load_all()

# df = datasets["financial_ratios.xlsx"]

# print(
#     df[
#         (df["company_id"] == "ABB") &
#         (df["year"] == 2024)
#     ]
# )