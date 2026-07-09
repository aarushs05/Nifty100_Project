import pandas as pd


def normalize_company_id(value):
    """Convert company IDs to uppercase and remove spaces."""
    if pd.isna(value):
        return None
    return str(value).strip().upper()

import pandas as pd

def normalize_text(value):
    if pd.isna(value):
        return None

    text = str(value)

    # Remove literal "\n"
    text = text.replace("\\n", " ")

    # Remove actual newline characters
    text = text.replace("\n", " ")

    # Remove carriage returns
    text = text.replace("\r", " ")

    # Collapse multiple spaces
    text = " ".join(text.split())

    return text

def normalize_numeric(value):
    """Convert values to numeric where possible."""
    return pd.to_numeric(value, errors="coerce")

def normalize_numeric(value):
    return pd.to_numeric(value, errors="coerce")

def normalize_year(value):
    """
    Extract a 4-digit year from different formats.
    Examples:
    Dec 2012 -> 2012
    Mar 2014 -> 2014
    2024 -> 2024
    """
import re
import pandas as pd

def normalize_year(value):
    """
    Normalize year values.

    Examples:
    Dec 2012 -> 2012
    Mar 2014 -> 2014
    Mar-13 -> 2013
    2024 -> 2024
    """

    if pd.isna(value):
        return None

    value = str(value).strip()

    # Match full year (2012, 2024)
    match = re.search(r"(20\d{2}|19\d{2})", value)
    if match:
        return int(match.group())

    # Match short year like Mar-13
    match = re.search(r"-(\d{2})$", value)
    if match:
        yy = int(match.group(1))
        return 2000 + yy if yy < 50 else 1900 + yy

    return value


def normalize_dataframe(df):

    df = df.copy()

    for col in df.columns:

        if "company_id" in col.lower():

            df[col] = df[col].apply(normalize_company_id)

        elif "year" in col.lower():

            df[col] = df[col].apply(normalize_year)

        elif df[col].dtype == object:

            df[col] = df[col].apply(normalize_text)

    return df