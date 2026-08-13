"""
Valuation API endpoints.

Sprint 6 - Day 40.
"""

import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "nifty100.db"

router = APIRouter(
    prefix="/market-cap",
    tags=["Valuation"],
)


def get_connection():
    """Return SQLite connection."""

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


@router.get("/{ticker}")
def valuation_history(
    ticker: str,
):
    """Return historical valuation data for a company."""

    connection = get_connection()

    try:

        company = connection.execute(
            """
            SELECT id, company_name
            FROM companies
            WHERE UPPER(id) = UPPER(?)
            """,
            (ticker,),
        ).fetchone()

        if company is None:
            raise HTTPException(
                status_code=404,
                detail=f"Company '{ticker}' not found.",
            )

        rows = connection.execute(
            """
            SELECT *
            FROM market_cap
            WHERE UPPER(company_id) = UPPER(?)
            AND year BETWEEN 2019 AND 2024
            ORDER BY year
            """,
            (ticker,),
        ).fetchall()

        return {
            "company_id": ticker.upper(),
            "company_name": company["company_name"],
            "from_year": 2019,
            "to_year": 2024,
            "count": len(rows),
            "history": [dict(row) for row in rows],
        }

    finally:
        connection.close()
