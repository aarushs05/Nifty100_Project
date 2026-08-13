"""
Portfolio statistics API.

Sprint 6 - Day 40.
"""

import sqlite3
from pathlib import Path

import pandas as pd
from fastapi import APIRouter

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "nifty100.db"

PORTFOLIO_FILE = PROJECT_ROOT / "output" / "portfolio_stats.csv"

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)


@router.get("/stats")
def portfolio_stats():
    """Return P10 through P90 statistics for core KPIs."""

    if PORTFOLIO_FILE.exists():

        df = pd.read_csv(PORTFOLIO_FILE)

        return {
            "count": len(df),
            "source": str(PORTFOLIO_FILE),
            "statistics": df.to_dict(orient="records"),
        }

    # Fallback: calculate directly from SQLite.
    connection = sqlite3.connect(DB_PATH)

    try:

        df = pd.read_sql_query(
            """
            SELECT *
            FROM financial_ratios
            """,
            connection,
        )

    finally:

        connection.close()

    metrics = [
        "return_on_equity_pct",
        "return_on_assets_pct",
        "return_on_capital_employed_pct",
        "debt_to_equity",
        "interest_coverage",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "asset_turnover",
        "fcf_conversion_pct",
        "dividend_payout_ratio_pct",
    ]

    rows = []

    for metric in metrics:

        values = pd.to_numeric(
            df[metric],
            errors="coerce",
        ).dropna()

        rows.append(
            {
                "kpi": metric,
                "P10": values.quantile(0.10),
                "P25": values.quantile(0.25),
                "P50": values.quantile(0.50),
                "P75": values.quantile(0.75),
                "P90": values.quantile(0.90),
                "Mean": values.mean(),
                "Std": values.std(),
            }
        )

    return {
        "count": len(rows),
        "statistics": rows,
    }
