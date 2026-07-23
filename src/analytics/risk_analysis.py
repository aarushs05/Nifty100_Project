"""
Sprint 3
Risk Analysis
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)


class RiskAnalysis:

    def __init__(self, scorecard):

        self.scorecard = scorecard.copy()

    def generate(self):

        df = self.scorecard.copy()

        # -----------------------------------------
        # Risk Score
        # Higher debt and lower interest coverage
        # means higher financial risk
        # -----------------------------------------

        df["risk_score"] = (

            df["debt_to_equity"].rank(pct=True) * 60

            +

            (1 - df["interest_coverage"].rank(pct=True)) * 40

        )

        # -----------------------------------------
        # Safest Companies
        # -----------------------------------------

        safest = (

            df

            .sort_values(

                "risk_score"

            )

            .head(20)

        )

        # -----------------------------------------
        # Riskiest Companies
        # -----------------------------------------

        riskiest = (

            df

            .sort_values(

                "risk_score",

                ascending=False

            )

            .head(20)

        )

        # -----------------------------------------
        # Save CSVs
        # -----------------------------------------

        safest.to_csv(

            OUTPUT / "lowest_risk_companies.csv",

            index=False

        )

        riskiest.to_csv(

            OUTPUT / "highest_risk_companies.csv",

            index=False

        )

        risk_summary = (

            df.groupby("broad_sector")

            .agg(

                average_risk=("risk_score", "mean"),

                average_debt=("debt_to_equity", "mean"),

                average_interest=("interest_coverage", "mean"),

                companies=("company_id", "count")

            )

            .reset_index()

            .sort_values(

                "average_risk",

                ascending=False

            )

        )

        risk_summary.to_csv(

            OUTPUT / "risk_summary.csv",

            index=False

        )

        print()

        print("=" * 70)

        print("RISK ANALYSIS")

        print("=" * 70)

        print()

        print("Top 10 Safest Companies")

        print(

            safest[

                [

                    "company_name",

                    "debt_to_equity",

                    "interest_coverage",

                    "risk_score"

                ]

            ].head(10)

        )

        print()

        print("Top 10 Highest Risk Companies")

        print(

            riskiest[

                [

                    "company_name",

                    "debt_to_equity",

                    "interest_coverage",

                    "risk_score"

                ]

            ].head(10)

        )

        print()

        return {

            "summary": risk_summary,

            "safe": safest,

            "risky": riskiest

        }