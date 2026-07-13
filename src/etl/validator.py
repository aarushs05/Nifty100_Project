import pandas as pd

from loader import ExcelLoader
from dq_rules import (
    dq01_primary_key,
    dq02_company_year,
    dq03_foreign_key,
    dq04_valid_year,
    dq05_positive_market_cap,
    dq06_financial_values,
    dq07_positive_prices,
    dq08_high_price,
    dq09_low_price,
    dq10_volume,
)

# ----------------------------
# Load all datasets
# ----------------------------

loader = ExcelLoader()
datasets = loader.load_all()
stock = datasets["stock_prices.xlsx"]

invalid = stock[
    (stock["high_price"] < stock["open_price"]) |
    (stock["high_price"] < stock["close_price"]) |
    (stock["high_price"] < stock["low_price"])
]

print(invalid.head(20))
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

    # DQ-02 Duplicate Company + Year
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

    # DQ-04 Valid Year
    failures.extend(
        dq04_valid_year(df, name)
    )

    # DQ-05 Positive Market Cap
    failures.extend(
        dq05_positive_market_cap(df, name)
    )

    # DQ-06 Financial Value Validation
    failures.extend(
        
        dq06_financial_values(df, name)
    )
        # DQ-07 Positive Stock Prices
    failures.extend(
        dq07_positive_prices(df, name)
    )

    # DQ-08 High Price Validation
    failures.extend(
        dq08_high_price(df, name)
    )

    # DQ-09 Low Price Validation
    failures.extend(
        dq09_low_price(df, name)
    )

    # DQ-10 Volume Validation
    failures.extend(
        dq10_volume(df, name)
    )
# ----------------------------
# Export Validation Report
# ----------------------------

failure_df = pd.DataFrame(failures)
print("\nDQ-06 Failures")
print(failure_df[failure_df["rule"] == "DQ-06"])
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