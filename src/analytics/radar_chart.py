"""
Sprint 3 - Peer Radar Chart

Generates a radar chart comparing one company
against the average of its broad sector.

Output:
output/radar/<company>_radar.png
"""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DB = "data/nifty100.db"

OUTPUT = Path("output/radar")
OUTPUT.mkdir(parents=True, exist_ok=True)


def load_data(company_id="TCS", year=2024):

    conn = sqlite3.connect(DB)

    query = """
    SELECT

        fr.company_id,

        c.company_name,

        s.broad_sector,

        fr.year,

        fr.return_on_equity_pct,

        fr.return_on_capital_employed_pct,

        fr.net_profit_margin_pct,

        fr.composite_quality_score

    FROM financial_ratios fr

    JOIN companies c
        ON fr.company_id = c.id

    JOIN sectors s
        ON fr.company_id = s.company_id

    WHERE fr.year = ?
    """

    df = pd.read_sql(query, conn, params=[year])

    conn.close()

    company = df[df["company_id"] == company_id]

    if company.empty:
        raise ValueError(
            f"{company_id} not found for year {year}"
        )

    sector = company.iloc[0]["broad_sector"]

    peers = df[df["broad_sector"] == sector]

    return company.iloc[0], peers


def create_radar(company_id="TCS", year=2024):

    company, peers = load_data(company_id, year)

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

    # Close polygon
    company_values += company_values[:1]
    peer_values += peer_values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False,
    ).tolist()

    angles += angles[:1]

    fig, ax = plt.subplots(
        figsize=(7, 7),
        subplot_kw={"polar": True},
    )

    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label=company_id,
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

    plt.title(
        f"{company['company_name']} vs Sector Average ({year})",
        fontsize=14,
        pad=20,
    )

    plt.legend(loc="upper right")

    file_path = OUTPUT / f"{company_id}_radar.png"

    plt.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"\n✓ Radar chart saved -> {file_path}")


def main():

    # Change company here if required
    create_radar(
        company_id="TCS",
        year=2024,
    )


if __name__ == "__main__":
    main()