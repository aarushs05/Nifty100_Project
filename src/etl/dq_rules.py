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
    Check duplicate (company_id, year) combinations.
    Only applies to datasets containing both columns.
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
                    f"company_id '{company}' "
                    f"not found in companies.xlsx"
)
            }
        )

    return failures

def dq03_foreign_key(df, companies_df, dataset_name):

    if "company_id" not in df.columns:
        return []

    failures = []

    valid_ids = set(
        companies_df["id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    invalid_ids = (
        df["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    invalid_ids = sorted(set(invalid_ids) - valid_ids)

    for company in invalid_ids:

        failures.append(
            {
                "rule": "DQ-03",
                "severity": "CRITICAL",
                "dataset": dataset_name,
                "row": "-",
                "message": f"Invalid company_id: {company}",
            }
        )

    return failures

