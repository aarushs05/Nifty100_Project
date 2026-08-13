"""
Company document API.

Sprint 6 - Day 40.
"""

import sqlite3
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import APIRouter, HTTPException

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "nifty100.db"

router = APIRouter(
    prefix="/companies",
    tags=["Documents"],
)


def get_connection():
    """Return SQLite connection."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def check_url(url):
    """Return whether a document URL is reachable."""

    if not url:
        return False

    try:
        request = Request(
            url,
            method="HEAD",
            headers={"User-Agent": "Mozilla/5.0 Nifty100-Analytics"},
        )

        with urlopen(
            request,
            timeout=5,
        ):
            return True

    except (
        HTTPError,
        URLError,
        TimeoutError,
        ValueError,
    ):
        return False


@router.get("/{ticker}/documents")
def company_documents(
    ticker: str,
):
    """Return annual report/document links with URL validity."""

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
            FROM documents
            WHERE UPPER(company_id) = UPPER(?)
            ORDER BY year
            """,
            (ticker,),
        ).fetchall()

        results = []

        for row in rows:
            record = dict(row)

            # Find likely URL/link column.
            url_value = None

            for key, value in record.items():
                if value is None:
                    continue

                key_lower = key.lower()

                if (
                    ("url" in key_lower or "link" in key_lower)
                    and isinstance(value, str)
                    and value.startswith(("http://", "https://"))
                ):
                    url_value = value
                    break

            record["is_url_valid"] = check_url(url_value)

            results.append(record)

        return {
            "company_id": ticker.upper(),
            "company_name": company["company_name"],
            "count": len(results),
            "documents": results,
        }

    finally:
        connection.close()