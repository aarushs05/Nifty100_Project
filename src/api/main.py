"""
Sprint 6 - FastAPI application.

Day 38:
- SQLite connection
- CORS middleware
- Request logging middleware
- API router registration
- Health endpoint
"""

import sqlite3
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "data" / "nifty100.db"


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Nifty100 Financial Analytics API",
    description=(
        "REST API for Nifty100 financial analytics, "
        "screening, valuation, peers and portfolio analysis."
    ),
    version="1.0.0",
)


# ============================================================
# APPLICATION START TIME
# ============================================================

START_TIME = time.time()


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATABASE CONNECTION
# ============================================================


def get_db_connection():
    """Return a SQLite database connection."""

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    connection = sqlite3.connect(
        DB_PATH,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# REQUEST LOGGING
# ============================================================


@app.middleware("http")
async def request_logging_middleware(
    request: Request,
    call_next,
):
    """Log HTTP method, path and response time."""

    start = time.perf_counter()

    response = await call_next(request)

    elapsed = time.perf_counter() - start

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"-> {response.status_code} "
        f"({elapsed:.4f}s)"
    )

    return response


# ============================================================
# HEALTH ENDPOINT
# ============================================================


@app.get(
    "/api/v1/health",
    tags=["Health"],
)
def health():
    """Return API status, database row counts, uptime and version."""

    connection = get_db_connection()

    tables = [
        "analysis",
        "balancesheet",
        "cashflow",
        "companies",
        "documents",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "profitandloss",
        "prosandcons",
    ]

    row_counts = {}

    try:

        for table in tables:

            cursor = connection.execute(f"SELECT COUNT(*) FROM [{table}]")

            row_counts[table] = cursor.fetchone()[0]

    finally:

        connection.close()

    return {
        "status": "ok",
        "db_row_counts": row_counts,
        "uptime_seconds": round(
            time.time() - START_TIME,
            2,
        ),
        "version": app.version,
    }


# ============================================================
# ROOT
# ============================================================


@app.get(
    "/",
    tags=["System"],
)
def root():
    """Return basic API information."""

    return {
        "name": "Nifty100 Financial Analytics API",
        "version": app.version,
        "docs": "/docs",
        "health": "/api/v1/health",
    }


# ============================================================
# ROUTERS
# ============================================================

from src.api.routers import (
    companies,
    documents,
    peers,
    portfolio,
    screener,
    sectors,
    valuation,
)

app.include_router(
    companies.router,
    prefix="/api/v1",
)

app.include_router(
    screener.router,
    prefix="/api/v1",
)

app.include_router(
    sectors.router,
    prefix="/api/v1",
)

app.include_router(
    peers.router,
    prefix="/api/v1",
)

app.include_router(
    valuation.router,
    prefix="/api/v1",
)

app.include_router(
    portfolio.router,
    prefix="/api/v1",
)

app.include_router(
    documents.router,
    prefix="/api/v1",
)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
