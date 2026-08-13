"""
Sprint 5 - Company Tearsheet Generator

Generates one PDF tearsheet for every company in the Nifty 100 database.

Output:
    reports/tearsheets/<company_id>.pdf
"""

import sqlite3
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
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

OUTPUT = ROOT / "reports" / "tearsheets"
OUTPUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPERS
# ============================================================


def safe_value(row, column, default="N/A"):
    """Safely retrieve a value from a pandas Series."""

    if row is None:
        return default

    try:
        value = row.get(column, default)
    except AttributeError:
        return default

    if pd.isna(value):
        return default

    if value == "":
        return default

    return value


def format_number(value, decimals=2):
    """Format numeric values safely."""

    if value is None:
        return "N/A"

    if pd.isna(value):
        return "N/A"

    try:
        return f"{float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return str(value)


def format_percent(value):
    """Format percentage values."""

    if value is None:
        return "N/A"

    if pd.isna(value):
        return "N/A"

    try:
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return str(value)


def format_url(value):
    """Return a safe URL string."""

    if value is None:
        return "N/A"

    if pd.isna(value):
        return "N/A"

    return str(value)


# ============================================================
# DATABASE LOADING
# ============================================================


def load_data():
    """
    Load all required data from SQLite.

    Returns:
        companies
        ratios
        sectors
        market
        pros_cons
    """

    conn = sqlite3.connect(DB)

    try:

        # ----------------------------------------------------
        # Companies
        # ----------------------------------------------------

        companies = pd.read_sql_query(
            """
            SELECT
                id,
                company_name,
                about_company,
                website,
                nse_profile,
                bse_profile,
                face_value,
                book_value,
                roce_percentage,
                roe_percentage
            FROM companies
            """,
            conn,
        )

        # ----------------------------------------------------
        # Financial Ratios
        # ----------------------------------------------------

        ratios = pd.read_sql_query(
            """
            SELECT *
            FROM financial_ratios
            """,
            conn,
        )

        # ----------------------------------------------------
        # Sectors
        # ----------------------------------------------------

        sectors = pd.read_sql_query(
            """
            SELECT *
            FROM sectors
            """,
            conn,
        )

        # ----------------------------------------------------
        # Market Cap / Valuation
        # ----------------------------------------------------

        market = pd.read_sql_query(
            """
            SELECT *
            FROM market_cap
            """,
            conn,
        )

        # ----------------------------------------------------
        # Pros & Cons
        # ----------------------------------------------------

        pros_cons = pd.read_sql_query(
            """
            SELECT *
            FROM prosandcons
            """,
            conn,
        )

    finally:
        conn.close()

    return (
        companies,
        ratios,
        sectors,
        market,
        pros_cons,
    )


# ============================================================
# PDF GENERATION
# ============================================================


def create_pdf(
    company,
    ratio,
    sector,
    market,
    pros_cons,
    output_path,
):
    """Create a single company tearsheet PDF."""

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    company_id = safe_value(company, "id")
    company_name = safe_value(
        company,
        "company_name",
        company_id,
    )

    # ========================================================
    # TITLE
    # ========================================================

    story.append(
        Paragraph(
            "NIFTY 100 COMPANY TEARSHEET",
            title_style,
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    story.append(
        Paragraph(
            f"<b>{company_name}</b> ({company_id})",
            heading_style,
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    # ========================================================
    # COMPANY DESCRIPTION
    # ========================================================

    story.append(
        Paragraph(
            "Company Overview",
            heading_style,
        )
    )

    description = safe_value(
        company,
        "about_company",
        "No company description available.",
    )

    description = str(description).replace(
        "\n",
        "<br/>",
    )

    story.append(
        Paragraph(
            description,
            body_style,
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    # ========================================================
    # COMPANY LINKS
    # ========================================================

    story.append(
        Paragraph(
            "Company Links",
            heading_style,
        )
    )

    links_data = [
        [
            "Website",
            format_url(
                safe_value(
                    company,
                    "website",
                )
            ),
        ],
        [
            "NSE",
            format_url(
                safe_value(
                    company,
                    "nse_profile",
                )
            ),
        ],
        [
            "BSE",
            format_url(
                safe_value(
                    company,
                    "bse_profile",
                )
            ),
        ],
    ]

    links_table = Table(
        links_data,
        colWidths=[
            1.2 * inch,
            5.8 * inch,
        ],
    )

    links_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
            ]
        )
    )

    story.append(links_table)

    story.append(Spacer(1, 0.2 * inch))

    # ========================================================
    # COMPANY SNAPSHOT
    # ========================================================

    story.append(
        Paragraph(
            "Company Snapshot",
            heading_style,
        )
    )

    snapshot = [
        [
            "Metric",
            "Value",
            "Metric",
            "Value",
        ],
        [
            "Face Value",
            format_number(
                safe_value(
                    company,
                    "face_value",
                )
            ),
            "Book Value",
            format_number(
                safe_value(
                    company,
                    "book_value",
                )
            ),
        ],
        [
            "ROE",
            format_percent(
                safe_value(
                    company,
                    "roe_percentage",
                )
            ),
            "ROCE",
            format_percent(
                safe_value(
                    company,
                    "roce_percentage",
                )
            ),
        ],
    ]

    snapshot_table = Table(
        snapshot,
        colWidths=[
            1.4 * inch,
            1.6 * inch,
            1.4 * inch,
            1.6 * inch,
        ],
    )

    snapshot_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
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

    story.append(snapshot_table)

    story.append(Spacer(1, 0.2 * inch))

    # ========================================================
    # FINANCIAL RATIOS
    # ========================================================

    story.append(
        Paragraph(
            "Financial Ratios",
            heading_style,
        )
    )

    ratio_data = [
        [
            "Metric",
            "Value",
        ],
        [
            "ROE",
            format_percent(
                safe_value(
                    ratio,
                    "return_on_equity_pct",
                )
            ),
        ],
        [
            "ROCE",
            format_percent(
                safe_value(
                    ratio,
                    "return_on_capital_employed_pct",
                )
            ),
        ],
        [
            "Net Profit Margin",
            format_percent(
                safe_value(
                    ratio,
                    "net_profit_margin_pct",
                )
            ),
        ],
        [
            "Operating Profit Margin",
            format_percent(
                safe_value(
                    ratio,
                    "operating_profit_margin_pct",
                )
            ),
        ],
        [
            "Debt / Equity",
            format_number(
                safe_value(
                    ratio,
                    "debt_to_equity",
                )
            ),
        ],
        [
            "Interest Coverage",
            format_number(
                safe_value(
                    ratio,
                    "interest_coverage",
                )
            ),
        ],
        [
            "Composite Quality Score",
            format_number(
                safe_value(
                    ratio,
                    "composite_quality_score",
                )
            ),
        ],
    ]

    ratio_table = Table(
        ratio_data,
        colWidths=[
            3.8 * inch,
            2.2 * inch,
        ],
    )

    ratio_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
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

    story.append(ratio_table)

    story.append(Spacer(1, 0.2 * inch))

    # ========================================================
    # SECTOR
    # ========================================================

    story.append(
        Paragraph(
            "Sector Information",
            heading_style,
        )
    )

    sector_data = [
        [
            "Broad Sector",
            str(
                safe_value(
                    sector,
                    "broad_sector",
                )
            ),
        ],
        [
            "Sub Sector",
            str(
                safe_value(
                    sector,
                    "sub_sector",
                )
            ),
        ],
        [
            "Market Cap Category",
            str(
                safe_value(
                    sector,
                    "market_cap_category",
                )
            ),
        ],
    ]

    sector_table = Table(
        sector_data,
        colWidths=[
            2.5 * inch,
            3.5 * inch,
        ],
    )

    sector_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
            ]
        )
    )

    story.append(sector_table)

    story.append(Spacer(1, 0.2 * inch))

    # ========================================================
    # MARKET VALUATION
    # ========================================================

    story.append(
        Paragraph(
            "Market Valuation",
            heading_style,
        )
    )

    valuation_data = [
        [
            "Metric",
            "Value",
        ],
        [
            "Market Cap (₹ Cr)",
            format_number(
                safe_value(
                    market,
                    "market_cap_crore",
                )
            ),
        ],
        [
            "P/E Ratio",
            format_number(
                safe_value(
                    market,
                    "pe_ratio",
                )
            ),
        ],
        [
            "P/B Ratio",
            format_number(
                safe_value(
                    market,
                    "pb_ratio",
                )
            ),
        ],
        [
            "Dividend Yield",
            format_percent(
                safe_value(
                    market,
                    "dividend_yield_pct",
                )
            ),
        ],
    ]

    valuation_table = Table(
        valuation_data,
        colWidths=[
            3.8 * inch,
            2.2 * inch,
        ],
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
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
            ]
        )
    )

    story.append(valuation_table)

    story.append(Spacer(1, 0.2 * inch))

    # ========================================================
    # PROS & CONS
    # ========================================================

    story.append(
        Paragraph(
            "Pros & Cons",
            heading_style,
        )
    )

    pros = safe_value(
        pros_cons,
        "pros",
        "No pros available.",
    )

    cons = safe_value(
        pros_cons,
        "cons",
        "No cons available.",
    )

    confidence = safe_value(
        pros_cons,
        "confidence_score",
        "N/A",
    )

    pros_cons_data = [
        [
            "Pros",
            "Cons",
        ],
        [
            str(pros),
            str(cons),
        ],
    ]

    pros_cons_table = Table(
        pros_cons_data,
        colWidths=[
            3.0 * inch,
            3.0 * inch,
        ],
    )

    pros_cons_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
            ]
        )
    )

    story.append(pros_cons_table)

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            f"Pros/Cons Confidence Score: "
            f"{format_number(confidence)}",
            body_style,
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # ========================================================
    # YEAR
    # ========================================================

    ratio_year = safe_value(
        ratio,
        "year",
        "N/A",
    )

    story.append(
        Paragraph(
            f"Financial Year: {ratio_year}",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Source: Nifty 100 project SQLite database.",
            body_style,
        )
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
    )

    document.build(story)


# ============================================================
# GENERATE ALL TEARSHEETS
# ============================================================


def generate_all_tearsheets():
    """Generate one PDF tearsheet for every company."""

    (
        companies,
        ratios,
        sectors,
        market,
        pros_cons,
    ) = load_data()

    if companies.empty:
        raise ValueError(
            "No companies found in database."
        )

    generated = 0
    skipped = 0

    print("=" * 70)
    print("NIFTY 100 TEARSHEET GENERATION")
    print("=" * 70)

    print(
        f"Companies found: {len(companies)}"
    )

    # --------------------------------------------------------
    # Generate company by company
    # --------------------------------------------------------

    for _, company in companies.iterrows():

        company_id = str(
            safe_value(
                company,
                "id",
            )
        )

        # ----------------------------------------------------
        # Latest ratio row
        # ----------------------------------------------------

        ratio_rows = ratios[
            ratios["company_id"].astype(str)
            == company_id
        ].copy()

        if not ratio_rows.empty:

            ratio_rows = ratio_rows.sort_values(
                "year",
                ascending=False,
            )

            ratio = ratio_rows.iloc[0]

        else:

            print(
                f"Warning {company_id}: "
                "no financial ratios available; using N/A values."
            )

            ratio = pd.Series(
                dtype=object
            )

        # ----------------------------------------------------
        # Sector
        # ----------------------------------------------------

        sector_rows = sectors[
            sectors["company_id"].astype(str)
            == company_id
        ]

        if not sector_rows.empty:
            sector = sector_rows.iloc[0]
        else:
            sector = pd.Series(
                dtype=object
            )

        # ----------------------------------------------------
        # Market valuation
        # ----------------------------------------------------

        market_rows = market[
            market["company_id"].astype(str)
            == company_id
        ].copy()

        if not market_rows.empty:

            if "year" in market_rows.columns:
                market_rows = market_rows.sort_values(
                    "year",
                    ascending=False,
                )

            market_row = market_rows.iloc[0]

        else:

            market_row = pd.Series(
                dtype=object
            )

        # ----------------------------------------------------
        # Pros & Cons
        # ----------------------------------------------------

        pros_cons_rows = pros_cons[
            pros_cons["company_id"].astype(str)
            == company_id
        ]

        if not pros_cons_rows.empty:
            pros_cons_row = pros_cons_rows.iloc[0]
        else:
            pros_cons_row = pd.Series(
                dtype=object
            )

        # ----------------------------------------------------
        # Output
        # ----------------------------------------------------

        output_path = (
            OUTPUT
            / f"{company_id}.pdf"
        )

        try:

            create_pdf(
                company,
                ratio,
                sector,
                market_row,
                pros_cons_row,
                output_path,
            )

            generated += 1

            print(
                f"Tearsheet generated: "
                f"{company_id} -> {output_path}"
            )

        except (OSError, ValueError, KeyError, TypeError) as exc:

            skipped += 1

            print(
                f"ERROR {company_id}: "
                f"{type(exc).__name__}: {exc}"
            )

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print("=" * 70)
    print("TEARSHEET GENERATION COMPLETE")
    print("=" * 70)
    print(
        f"Companies Found : {len(companies)}"
    )
    print(
        f"Generated       : {generated}"
    )
    print(
        f"Skipped         : {skipped}"
    )
    print(
        f"Output          : {OUTPUT}"
    )
    print("=" * 70)

    return generated


# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":
    generate_all_tearsheets()