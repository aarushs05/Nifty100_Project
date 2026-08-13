"""
Generate the Nifty 100 Analyst Guide PDF.

Output:
    docs/analyst_guide.pdf
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

OUTPUT = ROOT / "docs" / "analyst_guide.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


def build_pdf():
    """Generate the analyst guide PDF."""

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "GuideTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        leading=26,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "GuideHeading",
        parent=styles["Heading1"],
        fontSize=15,
        leading=19,
        spaceBefore=14,
        spaceAfter=8,
    )

    subheading_style = ParagraphStyle(
        "GuideSubheading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=15,
        spaceBefore=10,
        spaceAfter=5,
    )

    body_style = ParagraphStyle(
        "GuideBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=7,
    )

    bullet_style = ParagraphStyle(
        "GuideBullet",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-8,
        spaceAfter=4,
    )

    small_style = ParagraphStyle(
        "GuideSmall",
        parent=body_style,
        fontSize=8,
        leading=11,
    )

    story = []

    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "NIFTY 100 ANALYST GUIDE",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Financial Analytics, Screening, Valuation, Risk and Company Intelligence Platform",
            body_style,
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>Purpose:</b> This guide explains how an analyst can use "
            "the Nifty 100 analytics platform to review companies, compare "
            "sectors, evaluate valuation, assess risk, inspect cash-flow "
            "quality and access generated company reports.",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 1. PLATFORM OVERVIEW
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "1. Platform Overview",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "The platform combines structured financial data, financial "
            "ratio analysis, stock screening, peer analytics, valuation "
            "analysis, risk analysis, NLP-based insights, company "
            "tearsheets, sector reports, portfolio statistics, an "
            "interactive dashboard and a REST API.",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 2. DATA FOUNDATION
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "2. Data Foundation",
            heading_style,
        )
    )

    data_items = [
        "SQLite database: <b>data/nifty100.db</b>",
        "Company master information",
        "Profit and loss statements",
        "Balance sheets",
        "Cash-flow statements",
        "Financial ratios",
        "Market capitalization and valuation metrics",
        "Sector and peer-group information",
        "Historical stock prices",
        "Pros and cons and NLP-derived company insights",
    ]

    for item in data_items:
        story.append(
            Paragraph(
                f"• {item}",
                bullet_style,
            )
        )

    # ---------------------------------------------------------
    # 3. COMPANY ANALYSIS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "3. Company Analysis",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Use the company scorecard as the primary company-level "
            "starting point. It combines profitability, capital efficiency, "
            "cash-flow quality, leverage and market information.",
            body_style,
        )
    )

    metrics = [
        ["Metric", "Purpose"],
        ["ROE", "Measures return generated on shareholders' equity."],
        ["ROCE", "Measures efficiency of capital employed."],
        ["Net Margin", "Shows profitability after expenses."],
        ["Operating Margin", "Shows operating profitability."],
        ["Debt to Equity", "Indicates financial leverage."],
        ["Interest Coverage", "Indicates ability to service interest costs."],
        ["P/E", "Market valuation relative to earnings."],
        ["P/B", "Market valuation relative to book value."],
        ["Dividend Yield", "Cash dividend yield relative to market price."],
    ]

    table = Table(
        metrics,
        colWidths=[1.5 * inch, 4.8 * inch],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    story.append(table)

    # ---------------------------------------------------------
    # 4. STOCK SCREENER
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "4. Stock Screener",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "The stock screener allows analysts to narrow the Nifty 100 "
            "universe using financial and valuation criteria.",
            body_style,
        )
    )

    screener_items = [
        "Profitability and return metrics",
        "Leverage and financial strength",
        "Valuation metrics",
        "Market capitalization",
        "Quality-oriented ranking",
        "Sector-based filtering",
    ]

    for item in screener_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    # ---------------------------------------------------------
    # 5. VALUATION
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "5. Valuation Analysis",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Valuation analysis combines P/E, P/B and ROE ranking to "
            "identify companies with relatively attractive valuation "
            "characteristics. The system produces top valuation picks, "
            "undervalued companies and overvalued companies.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Important:</b> The valuation outputs are analytical "
            "screening results and should not be interpreted as investment "
            "recommendations by themselves.",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 6. RISK ANALYSIS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "6. Risk Analysis",
            heading_style,
        )
    )

    risk_items = [
        "Debt-to-equity",
        "Interest coverage",
        "Financial leverage",
        "Lowest-risk company ranking",
        "Highest-risk company ranking",
        "Risk summary",
    ]

    for item in risk_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    # ---------------------------------------------------------
    # 7. CASH FLOW INTELLIGENCE
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "7. Cash-Flow Intelligence",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Cash-flow intelligence evaluates operating, investing and "
            "financing cash-flow information and produces a cash-flow "
            "health classification, risk level, commentary and score.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Output: <b>output/cashflow_intelligence.xlsx</b> and "
            "<b>output/cashflow_insights.csv</b>.",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 8. NLP INSIGHTS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "8. NLP and Company Intelligence",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "The platform contains NLP-oriented outputs including "
            "company pros and cons, parsed historical analysis metrics "
            "and generated company intelligence.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Relevant outputs include "
            "<b>pros_cons_generated.csv</b> and "
            "<b>analysis_parsed.csv</b>.",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 9. RADAR AND PEER ANALYSIS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "9. Peer Radar Analysis",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Radar charts compare an individual company's ROE, ROCE, "
            "net margin and quality characteristics against its broad "
            "sector average.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Generated charts are stored under "
            "<b>reports/radar_charts/</b>.",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 10. COMPANY TEARSHEETS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "10. Company Tearsheets",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "A PDF tearsheet is generated for each company. The tearsheet "
            "provides a compact company-level analytical view and can be "
            "used as a quick research reference.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Location: <b>reports/tearsheets/</b>",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "The REST API also exposes company tearsheet retrieval.",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 11. SECTOR ANALYSIS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "11. Sector Analysis",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Sector analysis aggregates company-level scorecard "
            "information to provide sector-level profitability, leverage, "
            "valuation, market-capitalization and quality comparisons.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Generated sector reports are stored under "
            "<b>reports/sector/</b>.",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 12. PORTFOLIO ANALYSIS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "12. Portfolio Analysis",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Portfolio analytics provide aggregate portfolio-level "
            "statistics and capital-allocation analysis. The generated "
            "portfolio report is available under "
            "<b>reports/portfolio/</b>.",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 13. DASHBOARD
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "13. Interactive Dashboard",
            heading_style,
        )
    )

    dashboard_items = [
        "Home dashboard",
        "Company profiles",
        "Stock screener",
        "Sector analysis",
        "Valuation analysis",
        "Risk analysis",
        "Capital allocation",
        "Portfolio statistics",
        "NLP insights",
        "Company reports",
    ]

    for item in dashboard_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(
        Paragraph(
            "Launch command:",
            subheading_style,
        )
    )

    story.append(
        Paragraph(
            "<font name='Courier'>streamlit run src/dashboard/app.py</font>",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 14. REST API
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "14. REST API",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "The project provides a FastAPI-based REST API for accessing "
            "company, screening, valuation, peer, report and portfolio "
            "analytics.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Application entry point: "
            "<b>src/api/main.py</b>.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "API documentation is available through the generated "
            "OpenAPI specification in <b>docs/openapi.json</b>.",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 15. TESTING
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "15. Quality Assurance",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Run the complete automated test suite from the project root:",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "<font name='Courier'>python -m pytest -q</font>",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "A successful run should report all collected tests as passing.",
            body_style,
        )
    )

    # ---------------------------------------------------------
    # 16. RECOMMENDED ANALYST WORKFLOW
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "16. Recommended Analyst Workflow",
            heading_style,
        )
    )

    workflow = [
        "1. Start with the company profile and basic company information.",
        "2. Review the company scorecard and profitability metrics.",
        "3. Compare the company with its sector peers.",
        "4. Review valuation using P/E, P/B and ROE.",
        "5. Review leverage and interest coverage.",
        "6. Inspect cash-flow intelligence.",
        "7. Review the company tearsheet.",
        "8. Use sector reports for broader industry context.",
        "9. Use the screener to identify comparable companies.",
        "10. Use the dashboard or REST API for interactive/external access.",
    ]

    for item in workflow:
        story.append(Paragraph(item, bullet_style))

    # ---------------------------------------------------------
    # 17. INTERPRETATION NOTES
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "17. Interpretation Notes",
            heading_style,
        )
    )

    notes = [
        "Higher ROE and ROCE generally indicate stronger capital efficiency.",
        "Higher margins generally indicate stronger profitability.",
        "Higher debt-to-equity generally indicates greater leverage.",
        "Higher interest coverage generally indicates stronger debt-servicing capacity.",
        "Lower valuation multiples can indicate relatively lower valuation, but must be considered alongside business quality and growth.",
        "Sector averages should be interpreted within the context of the sector's business model.",
        "Missing data should be treated as unavailable rather than automatically interpreted as zero.",
        "Analytics outputs are decision-support tools and are not standalone investment recommendations.",
    ]

    for item in notes:
        story.append(Paragraph(f"• {item}", bullet_style))

    # ---------------------------------------------------------
    # 18. PROJECT OUTPUT LOCATIONS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "18. Key Output Locations",
            heading_style,
        )
    )

    paths = [
        ["Output", "Location"],
        ["Company scorecard", "output/company_scorecard.csv"],
        ["Sector summary", "output/sector_summary.csv"],
        ["Valuation outputs", "output/top_companies.csv"],
        ["Risk outputs", "output/risk_summary.csv"],
        ["Cash-flow intelligence", "output/cashflow_intelligence.xlsx"],
        ["Company tearsheets", "reports/tearsheets/"],
        ["Sector reports", "reports/sector/"],
        ["Portfolio report", "reports/portfolio/"],
        ["Radar charts", "reports/radar_charts/"],
        ["Analytics report", "output/analytics_report.txt"],
        ["API specification", "docs/openapi.json"],
    ]

    table = Table(
        paths,
        colWidths=[2.0 * inch, 4.3 * inch],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#f2f2f2")],
                ),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "End of Analyst Guide",
            small_style,
        )
    )

    document.build(story)

    print(f"Analyst guide generated: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()