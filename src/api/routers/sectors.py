"""
Sector API endpoints.

Sprint 6 - Day 40.
"""

import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "nifty100.db"

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"],
)


def get_connection():
    """Return SQLite connection."""

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


@router.get("")
def list_sectors():
    """Return all sectors with company count and financial medians."""

    connection = get_connection()

    try:

        query = """
            WITH latest AS (
                SELECT fr.*
                FROM financial_ratios fr
                INNER JOIN (
                    SELECT
                        company_id,
                        MAX(year) AS max_year
                    FROM financial_ratios
                    GROUP BY company_id
                ) x
                ON fr.company_id = x.company_id
                AND fr.year = x.max_year
            )

            SELECT
                s.broad_sector AS sector,
                COUNT(DISTINCT s.company_id) AS company_count,
                ROUND(
                    AVG(latest.return_on_equity_pct),
                    2
                ) AS median_roe,
                ROUND(
                    AVG(latest.debt_to_equity),
                    2
                ) AS median_de,
                NULL AS median_pe
            FROM sectors s

            LEFT JOIN latest
                ON latest.company_id = s.company_id

            GROUP BY s.broad_sector

            ORDER BY s.broad_sector
        """

        rows = connection.execute(query).fetchall()

        return {
            "count": len(rows),
            "sectors": [dict(row) for row in rows],
        }

    finally:
        connection.close()


@router.get("/{sector}/companies")
def companies_in_sector(
    sector: str,
):
    """Return companies belonging to a sector."""

    connection = get_connection()

    try:

        sector_row = connection.execute(
            """
            SELECT DISTINCT broad_sector
            FROM sectors
            WHERE LOWER(broad_sector) = LOWER(?)
            """,
            (sector,),
        ).fetchone()

        if sector_row is None:
            raise HTTPException(
                status_code=404,
                detail=f"Sector '{sector}' not found.",
            )

        query = """
            SELECT
                c.id AS company_id,
                c.company_name,
                s.broad_sector,
                s.sub_sector,
                s.market_cap_category,
                c.roe_percentage AS roe_pct,
                c.roce_percentage AS roce_pct,
                fr.year,
                fr.return_on_equity_pct,
                fr.debt_to_equity,
                fr.operating_profit_margin_pct,
                fr.revenue_cagr_5yr,
                fr.pat_cagr_5yr
            FROM companies c

            INNER JOIN sectors s
                ON s.company_id = c.id

            LEFT JOIN financial_ratios fr
                ON fr.company_id = c.id
                AND fr.year = (
                    SELECT MAX(fr2.year)
                    FROM financial_ratios fr2
                    WHERE fr2.company_id = c.id
                )

            WHERE LOWER(s.broad_sector) = LOWER(?)

            ORDER BY c.company_name
        """

        rows = connection.execute(
            query,
            (sector,),
        ).fetchall()

        return {
            "sector": sector_row["broad_sector"],
            "count": len(rows),
            "companies": [dict(row) for row in rows],
        }

    finally:
        connection.close()
