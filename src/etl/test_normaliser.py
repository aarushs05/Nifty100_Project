import sys
import os

sys.path.append(os.path.abspath("src/etl"))

from normaliser import (
    normalize_year,
    normalize_company_id,
    normalize_text,
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