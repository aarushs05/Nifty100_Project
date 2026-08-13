"""
Peer-group API endpoints.

Sprint 6 - Day 40.
"""

import sqlite3
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "nifty100.db"

router = APIRouter(
    prefix="/peers",
    tags=["Peers"],
)


METRICS = [
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


def get_connection():
    """Return SQLite connection."""

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def latest_ratios(connection):
    """Return latest ratio record for each company."""

    rows = connection.execute("""
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
        """).fetchall()

    return pd.DataFrame([dict(row) for row in rows])


@router.get("/{group_name}")
def peer_group(
    group_name: str,
):
    """Return peer companies with percentile ranks."""

    connection = get_connection()

    try:

        peer_rows = connection.execute(
            """
            SELECT
                peer_group_name,
                company_id,
                is_benchmark
            FROM peer_groups
            WHERE LOWER(peer_group_name) = LOWER(?)
            """,
            (group_name,),
        ).fetchall()

        if not peer_rows:
            raise HTTPException(
                status_code=404,
                detail=f"Peer group '{group_name}' not found.",
            )

        peers = pd.DataFrame([dict(row) for row in peer_rows])

        ratios = latest_ratios(connection)

        companies = pd.read_sql_query(
            """
            SELECT
                id AS company_id,
                company_name
            FROM companies
            """,
            connection,
        )

        data = peers.merge(
            companies,
            on="company_id",
            how="left",
        ).merge(
            ratios,
            on="company_id",
            how="left",
        )

        # ----------------------------------------------------
        # Percentile ranks
        # ----------------------------------------------------

        results = []

        for _, row in data.iterrows():

            record = {
                "company_id": row["company_id"],
                "company_name": row["company_name"],
                "is_benchmark": int(row["is_benchmark"]),
            }

            for metric in METRICS:

                values = pd.to_numeric(
                    data[metric],
                    errors="coerce",
                )

                value = row[metric]

                if pd.isna(value):
                    percentile = None
                else:
                    percentile = (
                        values.rank(
                            pct=True,
                            method="average",
                        ).loc[row.name]
                        * 100
                    )

                record[metric] = None if pd.isna(value) else float(value)

                record[f"{metric}_percentile"] = (
                    None
                    if percentile is None
                    else round(
                        float(percentile),
                        2,
                    )
                )

            results.append(record)

        return {
            "peer_group": peer_rows[0]["peer_group_name"],
            "count": len(results),
            "companies": results,
        }

    finally:
        connection.close()


@router.get(
    "/../companies/{ticker}/peers/compare",
)
def peer_compare(
    ticker: str,
):
    """
    Return radar comparison between company,
    peer average and benchmark.
    """

    connection = get_connection()

    try:

        company = connection.execute(
            """
            SELECT *
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

        peer = connection.execute(
            """
            SELECT
                peer_group_name
            FROM peer_groups
            WHERE UPPER(company_id) = UPPER(?)
            LIMIT 1
            """,
            (ticker,),
        ).fetchone()

        if peer is None:
            raise HTTPException(
                status_code=404,
                detail=f"No peer group found for '{ticker}'.",
            )

        group_name = peer["peer_group_name"]

        peer_rows = connection.execute(
            """
            SELECT
                company_id,
                is_benchmark
            FROM peer_groups
            WHERE peer_group_name = ?
            """,
            (group_name,),
        ).fetchall()

        ratios = latest_ratios(connection)

        company_ratios = ratios[ratios["company_id"].str.upper() == ticker.upper()]

        if company_ratios.empty:
            raise HTTPException(
                status_code=404,
                detail="Company ratios not found.",
            )

        peer_ids = [row["company_id"] for row in peer_rows]

        peer_data = ratios[ratios["company_id"].isin(peer_ids)]

        benchmark_ids = [row["company_id"] for row in peer_rows if row["is_benchmark"]]

        benchmark_data = ratios[ratios["company_id"].isin(benchmark_ids)]

        # Eight radar axes
        axes = METRICS[:8]

        radar = []

        for metric in axes:

            company_value = company_ratios[metric].iloc[0]

            peer_average = peer_data[metric].mean()

            benchmark_value = (
                benchmark_data[metric].mean() if not benchmark_data.empty else None
            )

            radar.append(
                {
                    "metric": metric,
                    "company": (
                        None if pd.isna(company_value) else float(company_value)
                    ),
                    "peer_group_average": (
                        None if pd.isna(peer_average) else float(peer_average)
                    ),
                    "benchmark": (
                        None
                        if benchmark_value is None or pd.isna(benchmark_value)
                        else float(benchmark_value)
                    ),
                }
            )

        return {
            "company_id": ticker.upper(),
            "peer_group": group_name,
            "radar": radar,
        }

    finally:
        connection.close()
