import pandas as pd


def dq01_primary_key(df, dataset_name, key_column="id"):
    """
    DQ-01
    Primary key uniqueness
    """

    failures = []

    duplicates = df[df.duplicated(subset=[key_column], keep=False)]

    for index, row in duplicates.iterrows():

        failures.append(
            {
                "rule": "DQ-01",
                "severity": "CRITICAL",
                "dataset": dataset_name,
                "row": index + 2,
                "message": f"Duplicate primary key: {row[key_column]}"
            }
        )

    return failures


def dq02_company_year(df, dataset_name):
    """
    DQ-02
    Duplicate (company_id, year)
    """

    if "company_id" not in df.columns or "year" not in df.columns:
        return []

    failures = []

    duplicate_rows = df[df.duplicated(
        subset=["company_id", "year"],
        keep=False
    )]

    for idx, row in duplicate_rows.iterrows():

        failures.append(
            {
                "rule": "DQ-02",
                "severity": "CRITICAL",
                "dataset": dataset_name,
                "row": idx + 2,
                "message": (
                    f"Duplicate company_id '{row['company_id']}' "
                    f"for year {row['year']}"
                )
            }
        )

    return failures


def dq03_foreign_key(df, companies_df, dataset_name):
    """
    DQ-03
    Foreign Key Validation
    """

    if "company_id" not in df.columns:
        return []

    failures = []

    valid_ids = set(
        companies_df["id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    company_ids = (
        df["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    invalid_ids = sorted(set(company_ids) - valid_ids)

    for company in invalid_ids:

        failures.append(
            {
                "rule": "DQ-03",
                "severity": "CRITICAL",
                "dataset": dataset_name,
                "row": "-",
                "message": f"Company ID '{company}' not found in companies.xlsx"
            }
        )

    return failures


def dq04_valid_year(df, dataset_name):
    """
    DQ-04
    Validate financial year.
    Ignore TTM values.
    """

    # detect year column
    if "year" in df.columns:
        year_col = "year"
    elif "Year" in df.columns:
        year_col = "Year"
    else:
        return []

    failures = []

    current_year = pd.Timestamp.today().year

    # Remove TTM rows before validation
    valid_df = df[
        df[year_col]
        .astype(str)
        .str.upper()
        != "TTM"
    ].copy()

    years = pd.to_numeric(valid_df[year_col], errors="coerce")

    invalid = valid_df[
        years.isna() |
        (years < 1990) |
        (years > current_year)
    ]

    for idx, row in invalid.iterrows():
        failures.append(
            {
                "rule": "DQ-04",
                "severity": "MAJOR",
                "dataset": dataset_name,
                "row": idx + 2,
                "message": f"Invalid year: {row[year_col]}"
            }
        )

    return failures


def dq05_positive_market_cap(df, dataset_name):
    """
    DQ-05
    Market Cap should be positive
    """

    if "market_cap_crore" not in df.columns:
        return []

    failures = []

    invalid = df[df["market_cap_crore"] <= 0]

    for idx, row in invalid.iterrows():

        failures.append(
            {
                "rule": "DQ-05",
                "severity": "CRITICAL",
                "dataset": dataset_name,
                "row": idx + 2,
                "message": f"Invalid Market Cap: {row['market_cap_crore']}"
            }
        )

    return failures

def dq06_financial_values(df, dataset_name):
    """
    DQ-06
    Values that must not be negative.
    """

    numeric_columns = [
    "debt_to_equity",
    "asset_turnover",
    "book_value_per_share",
    "total_debt_cr",
]

    numeric_columns = [
        col for col in numeric_columns
        if col in df.columns
    ]

    failures = []

    for col in numeric_columns:

        invalid = df[df[col] < 0]

        for idx, row in invalid.iterrows():

            failures.append(
                {
                    "rule": "DQ-06",
                    "severity": "WARNING",
                    "dataset": dataset_name,
                    "row": idx + 2,
                    "message": f"{col} cannot be negative ({row[col]})"
                }
            )

    return failures


def dq07_positive_prices(df, dataset_name):
    """
    DQ-07
    All stock prices must be greater than zero.
    """

    price_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "adjusted_close"
    ]

    if not all(col in df.columns for col in price_columns):
        return []

    failures = []

    for col in price_columns:

        invalid = df[df[col] <= 0]

        for idx, row in invalid.iterrows():

            failures.append(
                {
                    "rule": "DQ-07",
                    "severity": "CRITICAL",
                    "dataset": dataset_name,
                    "row": idx + 2,
                    "message": f"{col} must be greater than 0 (found {row[col]})"
                }
            )

    return failures

def dq08_high_price(df, dataset_name):
    """
    DQ-08
    High price must be the highest price of the day.
    """

    required = [
        "high_price",
        "open_price",
        "close_price",
        "low_price"
    ]

    if not all(col in df.columns for col in required):
        return []

    failures = []

    invalid = df[
        (df["high_price"] < df["open_price"]) |
        (df["high_price"] < df["close_price"]) |
        (df["high_price"] < df["low_price"])
    ]

    for idx, row in invalid.iterrows():

        failures.append(
            {
                "rule": "DQ-08",
                "severity": "MAJOR",
                "dataset": dataset_name,
                "row": idx + 2,
                "message": "High price is smaller than another day's price."
            }
        )

    return failures


def dq09_low_price(df, dataset_name):
    """
    DQ-09
    Low price must be the lowest price of the day.
    """

    required = [
        "low_price",
        "open_price",
        "close_price",
        "high_price"
    ]

    if not all(col in df.columns for col in required):
        return []

    failures = []

    invalid = df[
        (df["low_price"] > df["open_price"]) |
        (df["low_price"] > df["close_price"]) |
        (df["low_price"] > df["high_price"])
    ]

    for idx, row in invalid.iterrows():

        failures.append(
            {
                "rule": "DQ-09",
                "severity": "MAJOR",
                "dataset": dataset_name,
                "row": idx + 2,
                "message": "Low price is greater than another day's price."
            }
        )

    return failures


def dq10_volume(df, dataset_name):
    """
    DQ-10
    Trading volume must be positive.
    """

    if "volume" not in df.columns:
        return []

    failures = []

    invalid = df[df["volume"] <= 0]

    for idx, row in invalid.iterrows():

        failures.append(
            {
                "rule": "DQ-10",
                "severity": "CRITICAL",
                "dataset": dataset_name,
                "row": idx + 2,
                "message": f"Invalid trading volume: {row['volume']}"
            }
        )

    return failures