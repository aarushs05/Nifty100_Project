"""
Sprint 3
Valuation Analytics
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)


class ValuationAnalysis:

    def __init__(self, scorecard):

        self.scorecard = scorecard.copy()

    def generate(self):

        df = self.scorecard.copy()

        # -----------------------------------------
        # Remove companies without PE/PB
        # -----------------------------------------

        df = df.dropna(

            subset=[

                "pe_ratio",

                "pb_ratio"

            ]

        )

        # -----------------------------------------
        # Valuation Score
        # Lower PE/PB + Higher ROE = Better
        # -----------------------------------------

        df["valuation_score"] = (

            (1 - df["pe_ratio"].rank(pct=True)) * 40

            +

            (1 - df["pb_ratio"].rank(pct=True)) * 30

            +

            df["return_on_equity_pct"].rank(pct=True) * 30

        )

        # -----------------------------------------
        # Top Companies
        # -----------------------------------------

        top = (

            df

            .sort_values(

                "valuation_score",

                ascending=False

            )

            .head(20)

        )

        # -----------------------------------------
        # Undervalued
        # -----------------------------------------

        undervalued = (

            df

            .sort_values(

                [

                    "pe_ratio",

                    "pb_ratio"

                ],

                ascending=True

            )

            .head(20)

        )

        # -----------------------------------------
        # Overvalued
        # -----------------------------------------

        overvalued = (

            df

            .sort_values(

                [

                    "pe_ratio",

                    "pb_ratio"

                ],

                ascending=False

            )

            .head(20)

        )

        # -----------------------------------------
        # Save Files
        # -----------------------------------------

        top.to_csv(

            OUTPUT / "top_companies.csv",

            index=False

        )

        undervalued.to_csv(

            OUTPUT / "undervalued_companies.csv",

            index=False

        )

        overvalued.to_csv(

            OUTPUT / "overvalued_companies.csv",

            index=False

        )

        print()

        print("=" * 70)

        print("VALUATION ANALYSIS")

        print("=" * 70)

        print()

        print("Top Valuation Picks")

        print(

            top[

                [

                    "company_name",

                    "pe_ratio",

                    "pb_ratio",

                    "return_on_equity_pct",

                    "valuation_score"

                ]

            ]

        )

        print()

        return {

            "top": top,

            "undervalued": undervalued,

            "overvalued": overvalued

        }