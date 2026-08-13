import pandas as pd

from src.etl.dq_rules import (
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

# ============================================================
# DQ-01 — Primary Key
# ============================================================


def test_dq01_duplicate_primary_key():
    df = pd.DataFrame({"id": [1, 1, 2]})

    result = dq01_primary_key(df, "test.xlsx")

    assert len(result) == 2
    assert all(x["rule"] == "DQ-01" for x in result)
    assert all(x["severity"] == "CRITICAL" for x in result)


# ============================================================
# DQ-02 — Duplicate Company + Year
# ============================================================


def test_dq02_duplicate_company_year():
    df = pd.DataFrame(
        {"company_id": ["TCS", "TCS", "INFY"], "year": [2024, 2024, 2024]}
    )

    result = dq02_company_year(df, "financial_ratios.xlsx")

    assert len(result) == 2
    assert all(x["rule"] == "DQ-02" for x in result)
    assert all(x["severity"] == "CRITICAL" for x in result)


# ============================================================
# DQ-03 — Foreign Key
# ============================================================


def test_dq03_invalid_foreign_key():
    df = pd.DataFrame({"company_id": ["TCS", "INVALID"]})

    companies = pd.DataFrame({"id": ["TCS", "INFY"]})

    result = dq03_foreign_key(df, companies, "financial_ratios.xlsx")

    assert len(result) == 1
    assert result[0]["rule"] == "DQ-03"
    assert result[0]["severity"] == "CRITICAL"
    assert "INVALID" in result[0]["message"]


# ============================================================
# DQ-04 — Valid Year
# ============================================================


def test_dq04_invalid_year():
    df = pd.DataFrame({"year": [2024, 1980]})

    result = dq04_valid_year(df, "test.xlsx")

    assert len(result) == 1
    assert result[0]["rule"] == "DQ-04"
    assert result[0]["severity"] == "MAJOR"


# ============================================================
# DQ-05 — Positive Market Cap
# ============================================================


def test_dq05_negative_market_cap():
    df = pd.DataFrame({"market_cap_crore": [1000, -500]})

    result = dq05_positive_market_cap(df, "market_cap.xlsx")

    assert len(result) == 1
    assert result[0]["rule"] == "DQ-05"
    assert result[0]["severity"] == "CRITICAL"


# ============================================================
# DQ-06 — Financial Values
# ============================================================


def test_dq06_negative_financial_value():
    df = pd.DataFrame(
        {
            "debt_to_equity": [1.2, -0.5],
            "asset_turnover": [2.0, 1.5],
            "book_value_per_share": [100, 120],
            "total_debt_cr": [500, 600],
        }
    )

    result = dq06_financial_values(df, "financial_ratios.xlsx")

    assert len(result) == 1
    assert result[0]["rule"] == "DQ-06"
    assert result[0]["severity"] == "WARNING"


# ============================================================
# DQ-07 — Positive Prices
# ============================================================


def test_dq07_invalid_stock_price():
    df = pd.DataFrame(
        {
            "open_price": [100, 0],
            "high_price": [110, 105],
            "low_price": [90, 95],
            "close_price": [105, 100],
            "adjusted_close": [105, 100],
        }
    )

    result = dq07_positive_prices(df, "stock_prices.xlsx")

    assert len(result) == 1
    assert result[0]["rule"] == "DQ-07"
    assert result[0]["severity"] == "CRITICAL"


# ============================================================
# DQ-08 — High Price
# ============================================================


def test_dq08_invalid_high_price():
    df = pd.DataFrame(
        {
            "open_price": [100],
            "high_price": [90],
            "low_price": [80],
            "close_price": [95],
        }
    )

    result = dq08_high_price(df, "stock_prices.xlsx")

    assert len(result) == 1
    assert result[0]["rule"] == "DQ-08"
    assert result[0]["severity"] == "MAJOR"


# ============================================================
# DQ-09 — Low Price
# ============================================================


def test_dq09_invalid_low_price():
    df = pd.DataFrame(
        {
            "open_price": [100],
            "high_price": [110],
            "low_price": [105],
            "close_price": [95],
        }
    )

    result = dq09_low_price(df, "stock_prices.xlsx")

    assert len(result) == 1
    assert result[0]["rule"] == "DQ-09"
    assert result[0]["severity"] == "MAJOR"


# ============================================================
# DQ-10 — Volume
# ============================================================


def test_dq10_invalid_volume():
    df = pd.DataFrame({"volume": [10000, 0]})

    result = dq10_volume(df, "stock_prices.xlsx")

    assert len(result) == 1
    assert result[0]["rule"] == "DQ-10"
    assert result[0]["severity"] == "CRITICAL"


# ============================================================
# Additional edge/positive tests
# ============================================================


def test_dq01_valid_primary_key():
    df = pd.DataFrame({"id": [1, 2, 3]})

    result = dq01_primary_key(df, "test.xlsx")

    assert result == []


def test_dq03_valid_foreign_keys():
    df = pd.DataFrame({"company_id": ["TCS", "INFY"]})

    companies = pd.DataFrame({"id": ["TCS", "INFY"]})

    result = dq03_foreign_key(df, companies, "test.xlsx")

    assert result == []


def test_dq04_ttm_is_ignored():
    df = pd.DataFrame({"year": ["TTM", 2024]})

    result = dq04_valid_year(df, "test.xlsx")

    assert result == []


def test_dq10_valid_volume():
    df = pd.DataFrame({"volume": [100, 200, 500]})

    result = dq10_volume(df, "stock_prices.xlsx")

    assert result == []
