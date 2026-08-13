"""
Sprint 5 - Portfolio Summary Report

Generates the required Portfolio Summary PDF.

Input:
    output/portfolio_stats.csv

Output:
    reports/portfolio/portfolio_summary.pdf
"""

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

ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "output" / "portfolio_stats.csv"
OUTPUT_DIR = ROOT / "reports" / "portfolio"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def format_value(value):
    """Safely format a value for the PDF."""

    if value is None or pd.isna(value):
        return "N/A"

    if isinstance(value, float):
        return f"{value:,.2f}"

    return str(value)


def create_portfolio_report(df, output_path):
    """Create the portfolio summary PDF."""

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "NIFTY 100 PORTFOLIO SUMMARY",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "Portfolio-level analytical summary generated "
            "from the Nifty 100 project dataset.",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 20))

    # --------------------------------------------------------
    # Portfolio Statistics
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Portfolio Statistics",
            styles["Heading2"],
        )
    )

    statistics = []

    for column in df.columns:

        values = df[column].dropna()

        if values.empty:
            value = "N/A"

        elif pd.api.types.is_numeric_dtype(values):
            value = format_value(values.iloc[0])

        else:
            value = str(values.iloc[0])

        statistics.append(
            [
                str(column).replace("_", " ").title(),
                value,
            ]
        )

    if not statistics:
        statistics = [["Status", "No portfolio statistics available"]]

    table_data = [["Metric", "Value"]] + statistics

    table = Table(
        table_data,
        colWidths=[3.5 * 72, 2.5 * 72],
        repeatRows=1,
    )

    table.setStyle(
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
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
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

    story.append(table)

    story.append(Spacer(1, 24))

    # --------------------------------------------------------
    # Source Information
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "<b>Source:</b> output/portfolio_stats.csv",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "This report summarizes portfolio-level statistics "
            "calculated by the Nifty 100 analytics pipeline.",
            styles["BodyText"],
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


def generate_portfolio_report():
    """Load portfolio statistics and generate the PDF."""

    if not INPUT.exists():
        raise FileNotFoundError(
            f"Portfolio statistics file not found: {INPUT}"
        )

    df = pd.read_csv(INPUT)

    if df.empty:
        raise ValueError(
            "portfolio_stats.csv exists but contains no data."
        )

    output_path = OUTPUT_DIR / "portfolio_summary.pdf"

    create_portfolio_report(
        df,
        output_path,
    )

    print("=" * 70)
    print("PORTFOLIO REPORT GENERATED")
    print("=" * 70)
    print(f"Input  : {INPUT}")
    print(f"Output : {output_path}")
    print("=" * 70)

    return output_path


def main():
    """Main entry point."""

    generate_portfolio_report()


if __name__ == "__main__":
    main()