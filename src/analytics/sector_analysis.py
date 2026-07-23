"""
Sprint 3
Sector Analytics
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)


class SectorAnalysis:

    def __init__(
        self,
        scorecard
    ):

        self.scorecard = scorecard.copy()

    def generate(self):

        df = self.scorecard.copy()

        sector_summary = (

            df.groupby(

                "broad_sector"

            )

            .agg(

                companies=(

                    "company_id",
                    "count"

                ),

                avg_roe=(

                    "return_on_equity_pct",
                    "mean"

                ),

                avg_roce=(

                    "return_on_capital_employed_pct",
                    "mean"

                ),

                avg_net_margin=(

                    "net_profit_margin_pct",
                    "mean"

                ),

                avg_op_margin=(

                    "operating_profit_margin_pct",
                    "mean"

                ),

                avg_debt=(

                    "debt_to_equity",
                    "mean"

                ),

                avg_interest=(

                    "interest_coverage",
                    "mean"

                ),

                avg_pe=(

                    "pe_ratio",
                    "mean"

                ),

                avg_pb=(

                    "pb_ratio",
                    "mean"

                ),

                total_market_cap=(

                    "market_cap_crore",
                    "sum"

                ),

                avg_quality=(

                    "quality_rank",
                    "mean"

                )

            )

            .reset_index()

        )
        sector_summary = sector_summary.sort_values(

            by="avg_quality",

            ascending=False

        )

        sector_summary = sector_summary.round({

            "avg_roe": 2,

            "avg_roce": 2,

            "avg_net_margin": 2,

            "avg_op_margin": 2,

            "avg_debt": 2,

            "avg_interest": 2,

            "avg_pe": 2,

            "avg_pb": 2,

            "total_market_cap": 2,

            "avg_quality": 2

        })

        sector_summary.to_csv(

            OUTPUT / "sector_summary.csv",

            index=False

        )

        print()

        print("=" * 70)

        print("SECTOR SUMMARY")

        print("=" * 70)

        print(

            sector_summary

        )

        print()

        print(

            "Sector summary saved to "

            "output/sector_summary.csv"

        )

        return sector_summary