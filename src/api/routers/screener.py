"""
Nifty100 screener API.

Sprint 6 - Day 40.
"""

import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "nifty100.db"

router = APIRouter(
    prefix="/screener",
    tags=["Screener"],
)


def get_connection():
    """Return a SQLite connection."""

    if not DB_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="Database not found.",
        )

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


@router.get("")
def screen_companies(
    min_roe: float | None = Query(
        default=None,
        description="Minimum ROE percentage.",
    ),
    max_de: float | None = Query(
        default=None,
        description="Maximum debt-to-equity.",
    ),
    min_fcf: float | None = Query(
        default=None,
        description="Minimum free cash flow in crore.",
    ),
    sector: str | None = Query(
        default=None,
        description="Broad sector.",
    ),
    min_rev_cagr_5yr: float | None = Query(
        default=None,
        description="Minimum 5-year revenue CAGR percentage.",
    ),
    min_pat_cagr_5yr: float | None = Query(
        default=None,
        description="Minimum 5-year PAT CAGR percentage.",
    ),
    max_pe: float | None = Query(
        default=None,
        description="Maximum P/E.",
    ),
):
    """Screen and rank companies using financial filters."""

    numeric_parameters = {
        "min_roe": min_roe,
        "max_de": max_de,
        "min_fcf": min_fcf,
        "min_rev_cagr_5yr": min_rev_cagr_5yr,
        "min_pat_cagr_5yr": min_pat_cagr_5yr,
        "max_pe": max_pe,
    }

    for name, value in numeric_parameters.items():
        if value is not None and not isinstance(value, (int, float)):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid parameter: {name}",
            )

    if min_roe is not None and min_roe < -1000:
        raise HTTPException(
            status_code=400,
            detail="min_roe value is outside the valid range.",
        )

    if max_de is not None and max_de < 0:
        raise HTTPException(
            status_code=400,
            detail="max_de cannot be negative.",
        )

    if max_pe is not None and max_pe <= 0:
        raise HTTPException(
            status_code=400,
            detail="max_pe must be greater than zero.",
        )

    connection = get_connection()

    try:
        query = """
            SELECT
                fr.*,
                c.company_name,
                s.broad_sector,
                s.sub_sector,
                s.market_cap_category
            FROM financial_ratios fr

            INNER JOIN companies c
                ON c.id = fr.company_id

            LEFT JOIN sectors s
                ON s.company_id = fr.company_id

            WHERE fr.year = (
                SELECT MAX(fr2.year)
                FROM financial_ratios fr2
                WHERE fr2.company_id = fr.company_id
            )
        """

        rows = connection.execute(query).fetchall()

        records = [dict(row) for row in rows]

        filtered = []

        for record in records:
            if (
                sector is not None
                and str(record.get("broad_sector", "")).lower()
                != sector.lower()
            ):
                continue

            roe = record.get("return_on_equity_pct")
            de = record.get("debt_to_equity")
            fcf = record.get("free_cash_flow_cr")
            rev_cagr = record.get("revenue_cagr_5yr")
            pat_cagr = record.get("pat_cagr_5yr")

            # P/E is not currently stored in financial_ratios.
            pe = None

            if min_roe is not None and (roe is None or roe < min_roe):
                continue

            if max_de is not None and (de is None or de > max_de):
                continue

            if min_fcf is not None and (fcf is None or fcf < min_fcf):
                continue

            if min_rev_cagr_5yr is not None and (
                rev_cagr is None or rev_cagr < min_rev_cagr_5yr
            ):
                continue

            if min_pat_cagr_5yr is not None and (
                pat_cagr is None or pat_cagr < min_pat_cagr_5yr
            ):
                continue

            record["pe"] = pe

            filtered.append(record)

        filtered.sort(
            key=lambda x: (
                x.get("composite_quality_score")
                if x.get("composite_quality_score") is not None
                else -999999
            ),
            reverse=True,
        )

        for rank, record in enumerate(
            filtered,
            start=1,
        ):
            record["rank"] = rank

        return {
            "count": len(filtered),
            "filters": {
                "min_roe": min_roe,
                "max_de": max_de,
                "min_fcf": min_fcf,
                "sector": sector,
                "min_rev_cagr_5yr": min_rev_cagr_5yr,
                "min_pat_cagr_5yr": min_pat_cagr_5yr,
                "max_pe": max_pe,
            },
            "results": filtered,
        }

    finally:
        connection.close()