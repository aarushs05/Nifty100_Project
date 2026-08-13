"""
Company-related API endpoints.

Sprint 6 - Day 39.
"""

import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "nifty100.db"

TEARSHEET_DIR = PROJECT_ROOT / "reports" / "tearsheets"


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)


# ============================================================
# DATABASE
# ============================================================


def get_connection():
    """Return a SQLite database connection."""

    if not DB_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Database not found: {DB_PATH}",
        )

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# HELPERS
# ============================================================


def rows_to_dicts(rows):
    """Convert SQLite rows to dictionaries."""

    return [dict(row) for row in rows]


def get_company(
    connection,
    ticker: str,
):
    """Return a company record by ticker."""

    row = connection.execute(
        """
        SELECT *
        FROM companies
        WHERE UPPER(id) = UPPER(?)
        """,
        (ticker,),
    ).fetchone()

    return row


def parse_year(
    value: str | None,
):
    """Convert YYYY or YYYY-MM query values into integer years."""

    if value is None:
        return None

    value = value.strip()

    if len(value) == 7:
        # YYYY-MM
        try:
            return int(value[:4])
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=(f"Invalid year format: {value}. " "Use YYYY-MM."),
            )

    if len(value) == 4:
        try:
            return int(value)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=(f"Invalid year format: {value}. " "Use YYYY-MM."),
            )

    raise HTTPException(
        status_code=400,
        detail=(f"Invalid year format: {value}. " "Use YYYY-MM."),
    )


def validate_year_range(
    from_year: str | None,
    to_year: str | None,
):
    """Validate optional year range parameters."""

    start = parse_year(from_year)
    end = parse_year(to_year)

    if start is not None and end is not None and start > end:
        raise HTTPException(
            status_code=400,
            detail="from_year cannot be greater than to_year.",
        )

    return start, end


def company_exists(
    connection,
    ticker: str,
):
    """Raise HTTP 404 if ticker does not exist."""

    row = get_company(
        connection,
        ticker,
    )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found.",
        )

    return row


# ============================================================
# GET /companies
# ============================================================


@router.get("")
def list_companies(
    sector: str | None = Query(
        default=None,
        description="Filter by broad sector.",
    ),
    market_cap_category: str | None = Query(
        default=None,
        description="Filter by market-cap category.",
    ),
    search: str | None = Query(
        default=None,
        description="Partial company name or ticker search.",
    ),
):
    """
    Return all companies with basic financial and classification data.
    """

    connection = get_connection()

    try:

        query = """
            SELECT
                c.id AS company_id,
                c.company_name,
                s.broad_sector,
                s.sub_sector,
                s.market_cap_category,
                c.roe_percentage AS roe_pct,
                c.roce_percentage AS roce_pct
            FROM companies c
            LEFT JOIN sectors s
                ON c.id = s.company_id
            WHERE 1 = 1
        """

        params = []

        if sector:
            query += """
                AND LOWER(s.broad_sector) = LOWER(?)
            """

            params.append(sector.strip())

        if market_cap_category:
            query += """
                AND LOWER(s.market_cap_category) =
                    LOWER(?)
            """

            params.append(market_cap_category.strip())

        if search:
            query += """
                AND (
                    LOWER(c.company_name) LIKE LOWER(?)
                    OR LOWER(c.id) LIKE LOWER(?)
                )
            """

            search_pattern = f"%{search.strip()}%"

            params.extend(
                [
                    search_pattern,
                    search_pattern,
                ]
            )

        query += """
            ORDER BY c.company_name
        """

        rows = connection.execute(
            query,
            params,
        ).fetchall()

        return {
            "count": len(rows),
            "companies": rows_to_dicts(rows),
        }

    finally:
        connection.close()


# ============================================================
# GET /companies/{ticker}
# ============================================================


@router.get("/{ticker}")
def company_profile(
    ticker: str,
):
    """Return full company profile with latest KPIs and sector data."""

    connection = get_connection()

    try:

        company = company_exists(
            connection,
            ticker,
        )

        company_data = dict(company)

        # ----------------------------------------------------
        # Sector information
        # ----------------------------------------------------

        sector_rows = connection.execute(
            """
            SELECT
                company_id,
                broad_sector,
                sub_sector,
                index_weight_pct,
                market_cap_category
            FROM sectors
            WHERE company_id = ?
            """,
            (ticker.upper(),),
        ).fetchall()

        sector_data = rows_to_dicts(sector_rows)

        # ----------------------------------------------------
        # Latest financial ratios
        # ----------------------------------------------------

        latest_ratio = connection.execute(
            """
            SELECT *
            FROM financial_ratios
            WHERE company_id = ?
            ORDER BY year DESC
            LIMIT 1
            """,
            (ticker.upper(),),
        ).fetchone()

        latest_kpis = dict(latest_ratio) if latest_ratio else None

        return {
            "company": company_data,
            "latest_kpis": latest_kpis,
            "sector_data": sector_data,
        }

    finally:
        connection.close()


# ============================================================
# GET /companies/{ticker}/pl
# ============================================================


@router.get("/{ticker}/pl")
def company_profit_loss(
    ticker: str,
    from_year: str | None = Query(
        default=None,
        description="Starting year in YYYY-MM format.",
    ),
    to_year: str | None = Query(
        default=None,
        description="Ending year in YYYY-MM format.",
    ),
):
    """Return historical profit-and-loss records."""

    start, end = validate_year_range(
        from_year,
        to_year,
    )

    connection = get_connection()

    try:

        company_exists(
            connection,
            ticker,
        )

        query = """
            SELECT *
            FROM profitandloss
            WHERE company_id = ?
        """

        params = [ticker.upper()]

        if start is not None:
            query += """
                AND year >= ?
            """

            params.append(start)

        if end is not None:
            query += """
                AND year <= ?
            """

            params.append(end)

        query += """
            ORDER BY year
        """

        rows = connection.execute(
            query,
            params,
        ).fetchall()

        return {
            "company_id": ticker.upper(),
            "from_year": from_year,
            "to_year": to_year,
            "count": len(rows),
            "history": rows_to_dicts(rows),
        }

    finally:
        connection.close()


# ============================================================
# GET /companies/{ticker}/bs
# ============================================================


@router.get("/{ticker}/bs")
def company_balance_sheet(
    ticker: str,
    from_year: str | None = Query(
        default=None,
        description="Starting year in YYYY-MM format.",
    ),
    to_year: str | None = Query(
        default=None,
        description="Ending year in YYYY-MM format.",
    ),
):
    """Return historical balance-sheet records."""

    start, end = validate_year_range(
        from_year,
        to_year,
    )

    connection = get_connection()

    try:

        company_exists(
            connection,
            ticker,
        )

        query = """
            SELECT *
            FROM balancesheet
            WHERE company_id = ?
        """

        params = [ticker.upper()]

        if start is not None:
            query += """
                AND year >= ?
            """

            params.append(start)

        if end is not None:
            query += """
                AND year <= ?
            """

            params.append(end)

        query += """
            ORDER BY year
        """

        rows = connection.execute(
            query,
            params,
        ).fetchall()

        return {
            "company_id": ticker.upper(),
            "from_year": from_year,
            "to_year": to_year,
            "count": len(rows),
            "history": rows_to_dicts(rows),
        }

    finally:
        connection.close()


# ============================================================
# GET /companies/{ticker}/cashflow
# ============================================================


@router.get("/{ticker}/cashflow")
def company_cashflow(
    ticker: str,
    from_year: str | None = Query(
        default=None,
        description="Starting year in YYYY-MM format.",
    ),
    to_year: str | None = Query(
        default=None,
        description="Ending year in YYYY-MM format.",
    ),
):
    """Return historical cash-flow records."""

    start, end = validate_year_range(
        from_year,
        to_year,
    )

    connection = get_connection()

    try:

        company_exists(
            connection,
            ticker,
        )

        query = """
            SELECT *
            FROM cashflow
            WHERE company_id = ?
        """

        params = [ticker.upper()]

        if start is not None:
            query += """
                AND year >= ?
            """

            params.append(start)

        if end is not None:
            query += """
                AND year <= ?
            """

            params.append(end)

        query += """
            ORDER BY year
        """

        rows = connection.execute(
            query,
            params,
        ).fetchall()

        return {
            "company_id": ticker.upper(),
            "from_year": from_year,
            "to_year": to_year,
            "count": len(rows),
            "history": rows_to_dicts(rows),
        }

    finally:
        connection.close()


# ============================================================
# GET /companies/{ticker}/ratios
# ============================================================


@router.get("/{ticker}/ratios")
def company_ratios(
    ticker: str,
    year: int | None = Query(
        default=None,
        description="Optional financial year.",
    ),
):
    """Return computed financial KPIs for a company."""

    connection = get_connection()

    try:

        company_exists(
            connection,
            ticker,
        )

        query = """
            SELECT *
            FROM financial_ratios
            WHERE company_id = ?
        """

        params = [ticker.upper()]

        if year is not None:

            if year < 1900 or year > 2100:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid year.",
                )

            query += """
                AND year = ?
            """

            params.append(year)

        query += """
            ORDER BY year
        """

        rows = connection.execute(
            query,
            params,
        ).fetchall()

        return {
            "company_id": ticker.upper(),
            "year": year,
            "count": len(rows),
            "ratios": rows_to_dicts(rows),
        }

    finally:
        connection.close()


# ============================================================
# GET /companies/{ticker}/tearsheet
# ============================================================


@router.get(
    "/{ticker}/tearsheet",
)
def company_tearsheet(
    ticker: str,
):
    """Return the pre-generated company tearsheet PDF."""

    connection = get_connection()

    try:

        company_exists(
            connection,
            ticker,
        )

    finally:
        connection.close()

    ticker_upper = ticker.upper()

    # Expected naming convention:
    # reports/tearsheets/TCS.pdf
    pdf_path = TEARSHEET_DIR / f"{ticker_upper}.pdf"

    if not pdf_path.exists():

        raise HTTPException(
            status_code=404,
            detail=(f"Tearsheet PDF not found for " f"{ticker_upper}."),
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{ticker_upper}_tearsheet.pdf",
    )
