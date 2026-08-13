"""
Generate the Nifty 100 Project Acceptance Checklist PDF.

Output:
    docs/acceptance_checklist.pdf
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "acceptance_checklist.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


def check_exists(path):
    """Return PASS/MISSING based on whether a project path exists."""
    return "PASS" if (ROOT / path).exists() else "MISSING"


def build_pdf():
    """Generate the project acceptance checklist."""

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "AcceptanceTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=21,
        leading=25,
        spaceAfter=12,
    )

    heading_style = ParagraphStyle(
        "AcceptanceHeading",
        parent=styles["Heading1"],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=7,
    )

    body_style = ParagraphStyle(
        "AcceptanceBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        spaceAfter=6,
    )

    small_style = ParagraphStyle(
        "AcceptanceSmall",
        parent=body_style,
        fontSize=7.5,
        leading=10,
    )

    story = []

    # =========================================================
    # TITLE
    # =========================================================

    story.append(
        Paragraph(
            "NIFTY 100 PROJECT",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "FINAL ACCEPTANCE CHECKLIST",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Final verification document for the completed analytics, "
            "reporting, dashboard, NLP, machine-learning and REST API platform.",
            body_style,
        )
    )

    story.append(Spacer(1, 8))

    # =========================================================
    # PROJECT STATUS
    # =========================================================

    story.append(
        Paragraph(
            "1. Acceptance Status",
            heading_style,
        )
    )

    status_rows = [
        ["Area", "Acceptance Requirement", "Status"],
        [
            "Data Foundation",
            "SQLite database and core source tables available",
            check_exists("data/nifty100.db"),
        ],
        [
            "Financial Analytics",
            "Financial ratio engine and analytical outputs available",
            check_exists("output/financial_ratios.csv"),
        ],
        [
            "Company Analytics",
            "Company scorecard generated",
            check_exists("output/company_scorecard.csv"),
        ],
        [
            "Sector Analytics",
            "Sector summary generated",
            check_exists("output/sector_summary.csv"),
        ],
        [
            "Valuation",
            "Valuation outputs generated",
            check_exists("output/top_companies.csv"),
        ],
        [
            "Risk",
            "Risk outputs generated",
            check_exists("output/risk_summary.csv"),
        ],
        [
            "Cash Flow",
            "Cash-flow intelligence generated",
            check_exists("output/cashflow_intelligence.xlsx"),
        ],
        [
            "NLP",
            "Pros/cons and parsed analysis outputs available",
            check_exists("output/pros_cons_generated.csv"),
        ],
        [
            "Company Reports",
            "Company tearsheets generated",
            check_exists("reports/tearsheets"),
        ],
        [
            "Sector Reports",
            "Sector PDF reports generated",
            check_exists("reports/sector"),
        ],
        [
            "Portfolio",
            "Portfolio report generated",
            check_exists("reports/portfolio/portfolio_summary.pdf"),
        ],
        [
            "REST API",
            "FastAPI application available",
            check_exists("src/api/main.py"),
        ],
        [
            "Automated Tests",
            "Pytest report available",
            check_exists("reports/pytest_report.html"),
        ],
        [
            "Analyst Guide",
            "Analyst guide PDF available",
            check_exists("docs/analyst_guide.pdf"),
        ],
    ]

    table = Table(
        status_rows,
        colWidths=[1.25 * inch, 4.25 * inch, 0.75 * inch],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#f4f4f4")],
                ),
                ("ALIGN", (-1, 1), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    story.append(table)

    # =========================================================
    # CORE QUALITY CHECKS
    # =========================================================

    story.append(
        Paragraph(
            "2. Code Quality and Validation",
            heading_style,
        )
    )

    quality_checks = [
        [
            "Check",
            "Command / Evidence",
            "Expected Result",
        ],
        [
            "Ruff",
            "python -m ruff check src tests",
            "All checks passed",
        ],
        [
            "Pytest",
            "python -m pytest -q",
            "All tests pass",
        ],
        [
            "Database",
            "data/nifty100.db",
            "Database exists and is readable",
        ],
        [
            "API",
            "src/api/main.py",
            "FastAPI application available",
        ],
        [
            "OpenAPI",
            "docs/openapi.json",
            "API specification available",
        ],
    ]

    table = Table(
        quality_checks,
        colWidths=[1.0 * inch, 3.3 * inch, 1.95 * inch],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#f4f4f4")],
                ),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    story.append(table)

    # =========================================================
    # ANALYTICS ACCEPTANCE
    # =========================================================

    story.append(
        Paragraph(
            "3. Analytics Acceptance Criteria",
            heading_style,
        )
    )

    analytics_items = [
        "☐ Financial ratio engine produces populated financial ratio records.",
        "☐ Company scorecard contains profitability, leverage, valuation and quality metrics.",
        "☐ Sector analytics aggregate company-level metrics by broad sector.",
        "☐ Valuation analysis produces top, undervalued and overvalued company outputs.",
        "☐ Risk analysis produces safe/high-risk company outputs and risk summary.",
        "☐ Cash-flow intelligence produces health classification, risk level and cash-flow score.",
        "☐ NLP outputs contain generated company pros/cons and confidence scores.",
        "☐ Historical analysis parsing output is available.",
        "☐ Radar-chart analytics are available for company comparison.",
        "☐ Portfolio statistics/reporting output is available.",
    ]

    for item in analytics_items:
        story.append(
            Paragraph(
                item,
                body_style,
            )
        )

    # =========================================================
    # REPORTING ACCEPTANCE
    # =========================================================

    story.append(
        Paragraph(
            "4. Reporting Acceptance Criteria",
            heading_style,
        )
    )

    reporting_items = [
        "☐ Company tearsheets are generated under reports/tearsheets/.",
        "☐ Sector reports are generated under reports/sector/.",
        "☐ Portfolio summary PDF is available under reports/portfolio/.",
        "☐ Analytics text report is available under output/.",
        "☐ Analyst guide is available under docs/.",
        "☐ Reports can be consumed independently of the development environment.",
    ]

    for item in reporting_items:
        story.append(
            Paragraph(
                item,
                body_style,
            )
        )

    # =========================================================
    # DASHBOARD / API
    # =========================================================

    story.append(
        Paragraph(
            "5. Application Acceptance Criteria",
            heading_style,
        )
    )

    application_items = [
        "☐ Streamlit dashboard application is present.",
        "☐ Company profile functionality is available.",
        "☐ Stock screening functionality is available.",
        "☐ Sector analysis is available.",
        "☐ Valuation analysis is available.",
        "☐ Risk analysis is available.",
        "☐ Capital allocation and portfolio statistics are available.",
        "☐ NLP insights are available.",
        "☐ Company reports can be accessed.",
        "☐ FastAPI application is present and routers are registered.",
        "☐ OpenAPI specification is available.",
    ]

    for item in application_items:
        story.append(
            Paragraph(
                item,
                body_style,
            )
        )

    # =========================================================
    # DATA QUALITY
    # =========================================================

    story.append(
        Paragraph(
            "6. Data Quality Acceptance",
            heading_style,
        )
    )

    data_quality_items = [
        "☐ Primary-key validation implemented.",
        "☐ Company/year uniqueness validation implemented.",
        "☐ Foreign-key validation implemented.",
        "☐ Valid-year validation implemented.",
        "☐ Positive market-cap validation implemented.",
        "☐ Financial-value validation implemented.",
        "☐ Database contains the expected core analytical tables.",
    ]

    for item in data_quality_items:
        story.append(
            Paragraph(
                item,
                body_style,
            )
        )

    # =========================================================
    # FINAL TEST
    # =========================================================

    story.append(
        Paragraph(
            "7. Final Test Execution",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Final project validation should be performed from the project root.",
            body_style,
        )
    )

    commands = [
        "python -m ruff check src tests",
        "python -m pytest -q",
        "Test-Path data\\nifty100.db",
        "Test-Path src\\api\\main.py",
        "Test-Path reports\\pytest_report.html",
        "Test-Path docs\\analyst_guide.pdf",
        "Test-Path docs\\acceptance_checklist.pdf",
    ]

    for command in commands:
        story.append(
            Paragraph(
                f"• <font name='Courier'>{command}</font>",
                body_style,
            )
        )

    # =========================================================
    # FINAL ACCEPTANCE
    # =========================================================

    story.append(
        Paragraph(
            "8. Final Acceptance Decision",
            heading_style,
        )
    )

    acceptance_table = Table(
        [
            ["Criterion", "Decision"],
            ["Data foundation operational", "PASS / REVIEW"],
            ["Analytics operational", "PASS / REVIEW"],
            ["Reports generated", "PASS / REVIEW"],
            ["Dashboard/API available", "PASS / REVIEW"],
            ["Automated tests passing", "PASS / REVIEW"],
            ["Documentation complete", "PASS / REVIEW"],
            ["Overall project acceptance", "PASS / REVIEW"],
        ],
        colWidths=[4.6 * inch, 1.7 * inch],
        repeatRows=1,
    )

    acceptance_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                    colors.white,
                    colors.HexColor("#f4f4f4"),
                ]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(acceptance_table)

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Acceptance note: This checklist is intended as a final "
            "project-level verification document. Individual analytical "
            "outputs should be interpreted in the context of their source "
            "data and methodology.",
            small_style,
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "Nifty 100 Financial Analytics Project — Final QA",
            small_style,
        )
    )

    document.build(story)

    print(f"Acceptance checklist generated: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()