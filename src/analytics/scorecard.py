"""
Sprint 3
Company Scorecard
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)


class CompanyScorecard:

    def __init__(self, ratios, companies, sectors, market):

        self.ratios = ratios
        self.company = companies
        self.sector = sectors
        self.market = market

    def generate(self):

        latest_year = self.ratios["year"].max()

        df = self.ratios[
            self.ratios["year"] == latest_year
        ].copy()

        # ---------------------------------------------
        # Company Names
        # ---------------------------------------------

        df = df.merge(

            self.company[
                [
                    "id",
                    "company_name"
                ]
            ],

            left_on="company_id",
            right_on="id",

            how="left"

        )

        df.drop(
            columns="id",
            inplace=True
        )

        # ---------------------------------------------
        # Sector
        # ---------------------------------------------

        df = df.merge(

            self.sector[
                [
                    "company_id",
                    "broad_sector",
                    "sub_sector",
                    "market_cap_category"
                ]
            ],

            on="company_id",

            how="left"

        )

        # ---------------------------------------------
        # Market
        # ---------------------------------------------

        df = df.merge(

            self.market[
                [
                    "company_id",
                    "year",
                    "market_cap_crore",
                    "pe_ratio",
                    "pb_ratio",
                    "dividend_yield_pct"
                ]
            ],

            on=[
                "company_id",
                "year"
            ],

            how="left"

        )

        # ---------------------------------------------
        # Quality Rank
        # ---------------------------------------------

        df["quality_rank"] = (

            df["return_on_equity_pct"].rank(
                pct=True
            ) * 30

            +

            df["return_on_capital_employed_pct"].rank(
                pct=True
            ) * 25

            +

            df["net_profit_margin_pct"].rank(
                pct=True
            ) * 15

            +

            df["cfo_quality_score"].rank(
                pct=True
            ) * 15

            +

            (1 - df["debt_to_equity"].rank(
                pct=True
            )) * 15

        )

        scorecard = df[

            [

                "company_id",

                "company_name",

                "broad_sector",

                "sub_sector",

                "market_cap_category",

                "year",

                "return_on_equity_pct",

                "return_on_capital_employed_pct",

                "net_profit_margin_pct",

                "operating_profit_margin_pct",

                "debt_to_equity",

                "interest_coverage",

                "market_cap_crore",

                "pe_ratio",

                "pb_ratio",

                "dividend_yield_pct",

                "composite_quality_score",

                "quality_rank"

            ]

        ]

        scorecard = scorecard.sort_values(

            "quality_rank",

            ascending=False

        )

        scorecard.to_csv(

            OUTPUT / "company_scorecard.csv",

            index=False

        )

        print()

        print("=" * 70)

        print("Company Scorecard Generated")

        print("=" * 70)

        print(scorecard.head(10))

        print()

        return scorecard