"""
Sprint 3 - Peer Radar Charts

Generates radar charts for all companies in the Nifty 100 dataset.

Each company is compared against the average of its broad sector.
If 2024 financial-ratio data is unavailable, an explicit
data-unavailable radar chart is generated instead of inventing values.

Output:
reports/radar_charts/<company_id>_radar.png
"""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DB = Path("data/nifty100.db")

OUTPUT = Path("reports/radar_charts")
OUTPUT.mkdir(parents=True, exist_ok=True)


def load_data(year=2024):
    """Load all companies and available financial-ratio data."""

    conn = sqlite3.connect(DB)

    query = """
        SELECT
            c.id AS company_id,
            c.company_name,
            s.broad_sector,
            fr.year,
            fr.return_on_equity_pct,
            fr.return_on_capital_employed_pct,
            fr.net_profit_margin_pct,
            fr.composite_quality_score
        FROM companies c
        LEFT JOIN sectors s
            ON c.id = s.company_id
        LEFT JOIN financial_ratios fr
            ON c.id = fr.company_id
            AND fr.year = ?
        ORDER BY c.id
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=[year],
    )

    conn.close()

    return df


def create_unavailable_radar(company, output_path, year):
    """Create an explicit radar chart for unavailable data."""

    labels = [
        "ROE",
        "ROCE",
        "Net Margin",
        "Quality",
    ]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False,
    ).tolist()

    angles += angles[:1]

    values = [0] * len(labels)
    values += values[:1]

    _, ax = plt.subplots(
        figsize=(7, 7),
        subplot_kw={"polar": True},
    )

    ax.plot(
        angles,
        values,
        linewidth=2,
        linestyle="--",
        label="2024 data unavailable",
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_title(
        f"{company['company_name']} "
        f"({company['company_id']})\n"
        f"2024 Financial Ratio Data Unavailable",
        fontsize=14,
        pad=20,
    )

    ax.text(
        0.5,
        0.5,
        "DATA\nUNAVAILABLE",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=14,
    )

    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 1.1),
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def create_radar(company, peers, output_path):
    """Create a radar chart for one company."""

    peer_avg = peers.mean(numeric_only=True)

    labels = [
        "ROE",
        "ROCE",
        "Net Margin",
        "Quality",
    ]

    company_values = [
        company["return_on_equity_pct"],
        company["return_on_capital_employed_pct"],
        company["net_profit_margin_pct"],
        company["composite_quality_score"],
    ]

    peer_values = [
        peer_avg["return_on_equity_pct"],
        peer_avg["return_on_capital_employed_pct"],
        peer_avg["net_profit_margin_pct"],
        peer_avg["composite_quality_score"],
    ]

    company_values += company_values[:1]
    peer_values += peer_values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False,
    ).tolist()

    angles += angles[:1]

    _, ax = plt.subplots(
        figsize=(7, 7),
        subplot_kw={"polar": True},
    )

    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label=company["company_id"],
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25,
    )

    ax.plot(
        angles,
        peer_values,
        linewidth=2,
        label="Sector Average",
    )

    ax.fill(
        angles,
        peer_values,
        alpha=0.15,
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_title(
        f"{company['company_name']} vs Sector Average "
        f"({int(company['year'])})",
        fontsize=14,
        pad=20,
    )

    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.2, 1.1),
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def generate_all_radars(year=2024):
    """Generate radar charts for all Nifty 100 companies."""

    df = load_data(year)

    if df.empty:
        raise ValueError(
            "No companies found in database."
        )

    generated = 0
    unavailable = 0

    for company_id in df["company_id"].dropna().unique():

        company_rows = df[
            df["company_id"] == company_id
        ]

        company = company_rows.iloc[0]

        output_path = (
            OUTPUT / f"{company_id}_radar.png"
        )

        required_metrics = [
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "net_profit_margin_pct",
            "composite_quality_score",
        ]

        data_available = all(
            pd.notna(company[column])
            for column in required_metrics
        )

        if not data_available:
            create_unavailable_radar(
                company,
                output_path,
                year,
            )

            unavailable += 1

            print(
                f"Radar chart generated: "
                f"{company_id} -> {output_path} "
                f"(2024 data unavailable)"
            )

            continue

        sector = company["broad_sector"]

        peers = df[
            (df["broad_sector"] == sector)
            & df["return_on_equity_pct"].notna()
        ]

        if peers.empty:
            create_unavailable_radar(
                company,
                output_path,
                year,
            )

            unavailable += 1

            print(
                f"Radar chart generated: "
                f"{company_id} -> {output_path} "
                f"(sector data unavailable)"
            )

            continue

        create_radar(
            company,
            peers,
            output_path,
        )

        generated += 1

        print(
            f"Radar chart generated: "
            f"{company_id} -> {output_path}"
        )

    total = generated + unavailable

    print()
    print("=" * 60)
    print("RADAR CHART GENERATION COMPLETE")
    print("=" * 60)
    print(f"Year             : {year}")
    print(f"Companies        : {total}")
    print(f"Normal charts    : {generated}")
    print(f"Unavailable data : {unavailable}")
    print(f"Total PNG files  : {total}")
    print(f"Output           : {OUTPUT}")
    print("=" * 60)

    return total


def main():
    """Generate all Nifty 100 radar charts."""

    generate_all_radars(year=2024)


if __name__ == "__main__":
    main()