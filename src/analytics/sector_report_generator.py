"""
Sprint 5 - Sector Report Generator

Generates one PDF report for every sector represented
in the Nifty 100 dataset.

Output:
    reports/sector/<sector_name>.pdf
"""

import sqlite3
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

DB = ROOT / "data" / "nifty100.db"

OUTPUT = ROOT / "reports" / "sector"
OUTPUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPERS
# ============================================================


def safe_number(value, decimals=2):
    """Safely format numeric values."""

    if value is None or pd.isna(value):
        return "N/A"

    try:
        return f"{float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return "N/A"


def safe_filename(value):
    """Convert sector name into a safe filename."""

    name = str(value).strip()

    invalid_chars = '<>:"/\\|?*'

    for char in invalid_chars:
        name = name.replace(char, "_")

    name = name.replace(" ", "_")

    return name


# ============================================================
# DATA LOADING
# ============================================================


def load_data():
    """Load latest financial ratio and sector information."""

    conn = sqlite3.connect(DB)

    query = """
        SELECT
            fr.company_id,
            c.company_name,
            s.broad_sector,
            s.sub_sector,
            fr.year,
            fr.return_on_equity_pct,
            fr.return_on_capital_employed_pct,
            fr.net_profit_margin_pct,
            fr.operating_profit_margin_pct,
            fr.debt_to_equity,
            fr.interest_coverage,
            fr.composite_quality_score,
            m.market_cap_crore,
            m.pe_ratio,
            m.pb_ratio,
            m.dividend_yield_pct
        FROM financial_ratios fr

        JOIN companies c
            ON fr.company_id = c.id

        JOIN sectors s
            ON fr.company_id = s.company_id

        LEFT JOIN market_cap m
            ON fr.company_id = m.company_id
            AND fr.year = m.year

        WHERE fr.year = (
            SELECT MAX(year)
            FROM financial_ratios
        )
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# ============================================================
# PDF GENERATION
# ============================================================


def create_sector_pdf(sector_name, sector_df, output_path):
    """Create one PDF report for a sector."""

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "NIFTY 100 SECTOR REPORT",
            title_style,
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            f"<b>Sector:</b> {sector_name}",
            heading_style,
        )
    )

    story.append(Spacer(1, 8))

    latest_year = int(sector_df["year"].max())

    story.append(
        Paragraph(
            f"<b>Financial Year:</b> {latest_year}",
            body_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Companies:</b> {len(sector_df)}",
            body_style,
        )
    )

    story.append(Spacer(1, 18))

    # --------------------------------------------------------
    # Sector Statistics
    # --------------------------------------------------------

    avg_roe = sector_df["return_on_equity_pct"].mean()
    avg_roce = sector_df["return_on_capital_employed_pct"].mean()
    avg_net_margin = sector_df["net_profit_margin_pct"].mean()
    avg_op_margin = sector_df["operating_profit_margin_pct"].mean()
    avg_debt = sector_df["debt_to_equity"].mean()
    avg_interest = sector_df["interest_coverage"].mean()
    avg_quality = sector_df["composite_quality_score"].mean()

    market_cap = sector_df["market_cap_crore"].sum()

    story.append(
        Paragraph(
            "Sector Overview",
            heading_style,
        )
    )

    overview_data = [
        ["Metric", "Sector Average"],
        ["ROE", f"{safe_number(avg_roe)}%"],
        ["ROCE", f"{safe_number(avg_roce)}%"],
        ["Net Profit Margin", f"{safe_number(avg_net_margin)}%"],
        ["Operating Margin", f"{safe_number(avg_op_margin)}%"],
        ["Debt / Equity", safe_number(avg_debt)],
        ["Interest Coverage", safe_number(avg_interest)],
        ["Quality Score", safe_number(avg_quality)],
        ["Total Market Cap", f"{safe_number(market_cap)} Cr"],
    ]

    overview_table = Table(
        overview_data,
        colWidths=[3.2 * 72, 2.5 * 72],
    )

    overview_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "RIGHT",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ]
        )
    )

    story.append(overview_table)

    story.append(Spacer(1, 20))

    # --------------------------------------------------------
    # Company Table
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Companies in Sector",
            heading_style,
        )
    )

    company_data = [
        [
            "Company",
            "ROE %",
            "ROCE %",
            "Net Margin %",
            "D/E",
            "Quality",
        ]
    ]

    sorted_df = sector_df.sort_values(
        "composite_quality_score",
        ascending=False,
    )

    for _, row in sorted_df.iterrows():

        company_data.append(
            [
                str(row["company_name"])[:28],
                safe_number(row["return_on_equity_pct"]),
                safe_number(row["return_on_capital_employed_pct"]),
                safe_number(row["net_profit_margin_pct"]),
                safe_number(row["debt_to_equity"]),
                safe_number(row["composite_quality_score"]),
            ]
        )

    company_table = Table(
        company_data,
        repeatRows=1,
        colWidths=[
            2.25 * 72,
            0.75 * 72,
            0.75 * 72,
            1.05 * 72,
            0.65 * 72,
            0.75 * 72,
        ],
    )

    company_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey,
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "RIGHT",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ]
        )
    )

    story.append(company_table)

    story.append(Spacer(1, 20))

    # --------------------------------------------------------
    # Valuation
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Valuation Overview",
            heading_style,
        )
    )

    avg_pe = sector_df["pe_ratio"].mean()
    avg_pb = sector_df["pb_ratio"].mean()
    avg_dividend = sector_df["dividend_yield_pct"].mean()

    valuation_data = [
        ["Metric", "Average"],
        ["P/E Ratio", safe_number(avg_pe)],
        ["P/B Ratio", safe_number(avg_pb)],
        ["Dividend Yield", f"{safe_number(avg_dividend)}%"],
    ]

    valuation_table = Table(
        valuation_data,
        colWidths=[3.2 * 72, 2.5 * 72],
    )

    valuation_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "RIGHT",
                ),
            ]
        )
    )

    story.append(valuation_table)

    story.append(Spacer(1, 20))

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "This report is generated from the Nifty 100 project "
            "database. Market valuation data should be interpreted "
            "alongside the underlying financial metrics.",
            body_style,
        )
    )

    # --------------------------------------------------------
    # Build PDF
    # --------------------------------------------------------

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    document.build(story)


# ============================================================
# GENERATE ALL SECTOR REPORTS
# ============================================================


def generate_all_sector_reports():
    """Generate one PDF for every sector."""

    df = load_data()

    if df.empty:
        raise ValueError(
            "No financial data available for sector reports."
        )

    sectors = (
        df["broad_sector"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    generated = 0
    skipped = 0

    print("=" * 70)
    print("GENERATING NIFTY 100 SECTOR REPORTS")
    print("=" * 70)

    for sector_name in sectors:

        sector_df = df[
            df["broad_sector"].astype(str).str.strip()
            == sector_name
        ].copy()

        if sector_df.empty:
            skipped += 1
            continue

        filename = safe_filename(sector_name) + ".pdf"

        output_path = OUTPUT / filename

        try:
            create_sector_pdf(
                sector_name,
                sector_df,
                output_path,
            )

            generated += 1

            print(
                f"Sector report generated: "
                f"{sector_name} -> {output_path}"
            )

        except (OSError, ValueError, KeyError, sqlite3.Error) as exc:
            skipped += 1

            print(
                f"Sector report failed: "
                f"{sector_name} -> {exc}"
            )

    print()
    print("=" * 70)
    print("SECTOR REPORT GENERATION COMPLETE")
    print("=" * 70)
    print(f"Sectors found : {len(sectors)}")
    print(f"Generated     : {generated}")
    print(f"Skipped       : {skipped}")
    print(f"Output        : {OUTPUT}")
    print("=" * 70)

    return generated


# ============================================================
# MAIN
# ============================================================


def main():
    """Main entry point."""

    generate_all_sector_reports()


if __name__ == "__main__":
    main()