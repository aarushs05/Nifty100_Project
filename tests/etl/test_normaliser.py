import sys
import os

sys.path.append(os.path.abspath("src/etl"))

from normaliser import (
    normalize_year,
    normalize_company_id,
    normalize_text,
    normalize_numeric,
)


def test_year_dec():
    assert normalize_year("Dec 2012") == 2012


def test_year_mar():
    assert normalize_year("Mar 2018") == 2018


def test_year_short():
    assert normalize_year("Mar-13") == 2013


def test_year_integer():
    assert normalize_year(2024) == 2024


def test_company_upper():
    assert normalize_company_id("tcs") == "TCS"


def test_company_spaces():
    assert normalize_company_id("  hdfcbank ") == "HDFCBANK"


def test_text_spaces():
    assert normalize_text("  Hello   World  ") == "Hello World"


def test_text_newline():
    assert normalize_text("ABC\\nDEF") == "ABC DEF"

import pytest

@pytest.mark.parametrize(
    "value,expected",
    [
        ("Dec 2012", 2012),
        ("Mar 2014", 2014),
        ("Mar-13", 2013),
        ("Mar-24", 2024),
        ("2024", 2024),
        ("2020", 2020),
        ("2019", 2019),
        (" 2018 ", 2018),
        (2021, 2021),
        (2015.0, 2015),
        ("Jan 2000", 2000),
        ("FY 2022", 2022),
        ("FY2023", 2023),
        ("Year 2021", 2021),
        (None, None),
        ("", ""),
        ("Unknown", "Unknown"),
        ("ABC", "ABC"),
        ("Mar-99", 1999),
        ("Dec-01", 2001),
    ],
)
def test_normalize_year_param(value, expected):
    assert normalize_year(value) == expected

@pytest.mark.parametrize(
    "value,expected",
    [
        ("tcs", "TCS"),
        ("TCS", "TCS"),
        (" tcs ", "TCS"),
        ("infosys", "INFOSYS"),
        (" Infosys ", "INFOSYS"),
        ("reliance", "RELIANCE"),
        ("hdfcbank", "HDFCBANK"),
        ("axisbank", "AXISBANK"),
        ("lt", "LT"),
        ("sbilife", "SBILIFE"),
        ("icicibank", "ICICIBANK"),
        ("abb", "ABB"),
        ("", ""),
        ("   ", ""),
        (None, None),
    ],
)
def test_normalize_company_id_param(value, expected):
    assert normalize_company_id(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (" Hello World ", "Hello World"),
        ("ABC\\nDEF", "ABC DEF"),
        ("ABC\nDEF", "ABC DEF"),
        ("ABC\rDEF", "ABC DEF"),
        (None, None),
    ],
)
def test_normalize_text_param(value, expected):
    assert normalize_text(value) == expected

import pandas as pd

@pytest.mark.parametrize(
    "value,expected",
    [
        ("123", 123),
        ("123.45", 123.45),
        (100, 100),
        ("ABC", float("nan")),
        (None, float("nan")),
    ],
)
def test_normalize_numeric_param(value, expected):
    result = normalize_numeric(value)

    if pd.isna(expected):
        assert pd.isna(result)
    else:
        assert result == expected