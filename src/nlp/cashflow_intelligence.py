"""
Sprint 5 - Cash Flow Intelligence

Generates:
    output/cashflow_insights.csv
    output/cashflow_intelligence.xlsx
"""

import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

DB = ROOT / "data" / "nifty100.db"
OUTPUT = ROOT / "output"

OUTPUT.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load Data
# --------------------------------------------------

conn = sqlite3.connect(DB)

cashflow_df = pd.read_sql(
    "SELECT * FROM cashflow",
    conn,
)

ratios_df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn,
)

conn.close()


# --------------------------------------------------
# Latest Row Per Company
# --------------------------------------------------

latest_cashflow = (
    cashflow_df
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)

latest_ratios = (
    ratios_df
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)


# --------------------------------------------------
# Merge Data
# --------------------------------------------------

merged_df = pd.merge(
    latest_cashflow,
    latest_ratios,
    on="company_id",
    how="inner",
)

print(f"Companies found: {len(merged_df)}")


# --------------------------------------------------
# Cash Flow Intelligence Engine
# --------------------------------------------------

results = []


for _, row in merged_df.iterrows():

    company_id = row["company_id"]

    comments = []

    score = 50

    # ----------------------------------------------
    # Operating Cash Flow
    # ----------------------------------------------

    operating_cf = row.get("operating_activity")

    if pd.notna(operating_cf):

        if operating_cf > 0:
            comments.append(
                "Operating cash flow remains positive."
            )
            score += 20

        elif operating_cf < 0:
            comments.append(
                "Negative operating cash flow is a warning sign."
            )
            score -= 20

    # ----------------------------------------------
    # FCF Conversion
    # ----------------------------------------------

    fcf_conversion = row.get("fcf_conversion_pct")

    if pd.notna(fcf_conversion):

        if fcf_conversion > 80:
            comments.append(
                "Business converts profits into cash efficiently."
            )
            score += 15

        elif fcf_conversion < 50:
            comments.append(
                "Weak cash conversion may impact future growth."
            )
            score -= 15

    # ----------------------------------------------
    # CFO Quality
    # ----------------------------------------------

    cfo_quality = row.get("cfo_quality_score")

    if pd.notna(cfo_quality):

        if cfo_quality > 70:
            comments.append(
                "Cash flow quality appears healthy."
            )
            score += 15

        elif cfo_quality < 40:
            comments.append(
                "Reported earnings may not be strongly "
                "supported by cash generation."
            )
            score -= 15

    # ----------------------------------------------
    # Clamp Score
    # ----------------------------------------------

    score = max(0, min(100, score))

    # ----------------------------------------------
    # Risk Level
    # ----------------------------------------------

    if score >= 75:
        risk_level = "LOW"

    elif score >= 50:
        risk_level = "MEDIUM"

    else:
        risk_level = "HIGH"

    # ----------------------------------------------
    # Health Category
    # ----------------------------------------------

    if score >= 80:
        health = "Excellent"

    elif score >= 65:
        health = "Strong"

    elif score >= 50:
        health = "Average"

    elif score >= 35:
        health = "Weak"

    else:
        health = "Poor"

    # ----------------------------------------------
    # Save Result
    # ----------------------------------------------

    results.append(
        {
            "company_id": company_id,
            "cashflow_health": health,
            "cashflow_comment": " ".join(comments),
            "risk_level": risk_level,
            "cashflow_score": score,
        }
    )


# --------------------------------------------------
# Output DataFrame
# --------------------------------------------------

cashflow_insights_df = pd.DataFrame(results)


# --------------------------------------------------
# CSV Output
# --------------------------------------------------

csv_output = OUTPUT / "cashflow_insights.csv"

cashflow_insights_df.to_csv(
    csv_output,
    index=False,
)


# --------------------------------------------------
# D-13 Excel Deliverable
# --------------------------------------------------

excel_output = OUTPUT / "cashflow_intelligence.xlsx"

with pd.ExcelWriter(
    excel_output,
    engine="openpyxl",
) as writer:

    # Complete intelligence output
    cashflow_insights_df.to_excel(
        writer,
        sheet_name="Cash Flow Intelligence",
        index=False,
    )

    # Low-risk companies
    cashflow_insights_df[
        cashflow_insights_df["risk_level"] == "LOW"
    ].to_excel(
        writer,
        sheet_name="Low Risk",
        index=False,
    )

    # Medium-risk companies
    cashflow_insights_df[
        cashflow_insights_df["risk_level"] == "MEDIUM"
    ].to_excel(
        writer,
        sheet_name="Medium Risk",
        index=False,
    )

    # High-risk companies
    cashflow_insights_df[
        cashflow_insights_df["risk_level"] == "HIGH"
    ].to_excel(
        writer,
        sheet_name="High Risk",
        index=False,
    )


# --------------------------------------------------
# Console Output
# --------------------------------------------------

print(
    f"Companies processed: "
    f"{len(cashflow_insights_df)}"
)

print(
    f"CSV output saved: "
    f"{csv_output}"
)

print(
    f"Excel output saved: "
    f"{excel_output}"
)

print("\nSample Output:\n")

print(
    cashflow_insights_df.head(10)
)