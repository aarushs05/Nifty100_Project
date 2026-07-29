"""
Dashboard Database Utilities
Sprint 4

Shared database helper functions for Streamlit.
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import streamlit as st

# -------------------------------------------------------
# Project Root
# -------------------------------------------------------

ROOT = Path(__file__).resolve().parents[3]

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.database.sqlite import SQLiteDB


# -------------------------------------------------------
# Generic SQL Query
# -------------------------------------------------------

@st.cache_data(ttl=600)
def run_query(sql: str, params=None):

    db = SQLiteDB()

    try:

        df = pd.read_sql_query(
            sql,
            db.conn,
            params=params
        )

    finally:

        db.close()

    return df


# -------------------------------------------------------
# Companies
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_companies():

    sql = """

    SELECT *

    FROM companies

    ORDER BY company_name

    """

    return run_query(sql)


# -------------------------------------------------------
# Company Profile
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_company_profile(company_id):

    sql = """

    SELECT *

    FROM companies

    WHERE id = ?

    """

    df = run_query(sql, [company_id])

    if len(df):

        return df.iloc[0]

    return None


# -------------------------------------------------------
# Available Years
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_years():

    sql = """

    SELECT DISTINCT year

    FROM financial_ratios

    ORDER BY year DESC

    """

    return run_query(sql)["year"].tolist()


# -------------------------------------------------------
# Financial Ratios
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_ratios(company_id, year=None):

    sql = """

    SELECT *

    FROM financial_ratios

    WHERE company_id = ?

    """

    params = [company_id]

    if year is not None:

        sql += """

        AND year = ?

        """

        params.append(year)

    sql += """

    ORDER BY year

    """

    return run_query(sql, params)


# -------------------------------------------------------
# Analysis Table
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_analysis(company_id):

    sql = """

    SELECT *

    FROM analysis

    WHERE company_id = ?

    """

    return run_query(sql, [company_id])
    # -------------------------------------------------------
# Profit & Loss
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_pl(company_id):

    sql = """

    SELECT *

    FROM profitandloss

    WHERE company_id = ?

    ORDER BY year

    """

    return run_query(sql, [company_id])


# -------------------------------------------------------
# Balance Sheet
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_bs(company_id):

    sql = """

    SELECT *

    FROM balancesheet

    WHERE company_id = ?

    ORDER BY year

    """

    return run_query(sql, [company_id])


# -------------------------------------------------------
# Cash Flow
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_cf(company_id):

    sql = """

    SELECT *

    FROM cashflow

    WHERE company_id = ?

    ORDER BY year

    """

    return run_query(sql, [company_id])


# -------------------------------------------------------
# Market Cap
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_market_cap(company_id):

    sql = """

    SELECT *

    FROM market_cap

    WHERE company_id = ?

    ORDER BY year

    """

    return run_query(sql, [company_id])


# -------------------------------------------------------
# Latest Market Cap
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_latest_market_cap(company_id):

    sql = """

    SELECT *

    FROM market_cap

    WHERE company_id = ?

    ORDER BY year DESC

    LIMIT 1

    """

    df = run_query(sql, [company_id])

    if len(df):

        return df.iloc[0]

    return None


# -------------------------------------------------------
# Sector Information
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_sectors():

    sql = """

    SELECT *

    FROM sectors

    ORDER BY broad_sector,
             sub_sector

    """

    return run_query(sql)


@st.cache_data(ttl=600)
def get_company_sector(company_id):

    sql = """

    SELECT *

    FROM sectors

    WHERE company_id = ?

    """

    df = run_query(sql, [company_id])

    if len(df):

        return df.iloc[0]

    return None
    # -------------------------------------------------------
# Peer Groups
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_peer_groups():

    sql = """
    SELECT DISTINCT peer_group_name
    FROM peer_groups
    ORDER BY peer_group_name
    """

    return run_query(sql)


@st.cache_data(ttl=600)
def get_peers(peer_group):

    sql = """
    SELECT *
    FROM peer_groups
    WHERE peer_group_name = ?
    """

    return run_query(sql, [peer_group])


# -------------------------------------------------------
# Pros & Cons
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_pros_cons(company_id):

    sql = """
    SELECT *
    FROM prosandcons
    WHERE company_id = ?
    """

    return run_query(sql, [company_id])


# -------------------------------------------------------
# Annual Reports
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_reports(company_id):

    sql = """
    SELECT *
    FROM documents
    WHERE company_id = ?
    ORDER BY Year DESC
    """

    return run_query(sql, [company_id])


# -------------------------------------------------------
# Dashboard Summary
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_dashboard_data():

    sql = """
    SELECT
        fr.company_id,
        c.company_name,
        s.broad_sector,
        fr.year,
        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.composite_quality_score
    FROM financial_ratios fr
    LEFT JOIN companies c
        ON fr.company_id = c.id
    LEFT JOIN sectors s
        ON fr.company_id = s.company_id
    """

    return run_query(sql)


# -------------------------------------------------------
# Valuation
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_valuation(company_id):

    sql = """
    SELECT *
    FROM market_cap
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 1
    """

    df = run_query(sql, [company_id])

    if len(df):
        return df.iloc[0]

    return None