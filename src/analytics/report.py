"""
Sprint 3
Analytics Report Generator
"""

from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)


class AnalyticsReport:

    def __init__(self, scorecard, sector, valuation, risk):

        self.scorecard = scorecard
        self.sector = sector
        self.valuation = valuation
        self.risk = risk

    def generate(self):

        report = []

        report.append("=" * 80)
        report.append("NIFTY 100 ANALYTICS REPORT")
        report.append("=" * 80)
        report.append("")
        report.append(f"Generated : {datetime.now()}")
        report.append("")
        report.append(f"Companies Analysed : {len(self.scorecard)}")
        report.append(f"Sectors Analysed   : {len(self.sector)}")
        report.append("")

        report.append("=" * 80)
        report.append("TOP 10 COMPANIES")
        report.append("=" * 80)

        for _, row in self.scorecard.head(10).iterrows():

            report.append(

                f"{row.company_name}"
                f" | ROE={row.return_on_equity_pct:.2f}%"
                f" | ROCE={row.return_on_capital_employed_pct:.2f}%"
                f" | Quality={row.quality_rank:.2f}"

            )

        report.append("")
        report.append("=" * 80)
        report.append("TOP SECTORS")
        report.append("=" * 80)

        for _, row in self.sector.head(10).iterrows():

            report.append(

                f"{row.broad_sector}"
                f" | Avg Quality={row.avg_quality:.2f}"

            )

        report.append("")
        report.append("=" * 80)
        report.append("BEST VALUATION PICKS")
        report.append("=" * 80)

        for _, row in self.valuation["top"].head(10).iterrows():

            report.append(

                f"{row.company_name}"
                f" | PE={row.pe_ratio:.2f}"
                f" | PB={row.pb_ratio:.2f}"
                f" | Score={row.valuation_score:.2f}"

            )

        report.append("")
        report.append("=" * 80)
        report.append("LOWEST RISK COMPANIES")
        report.append("=" * 80)

        for _, row in self.risk["safe"].head(10).iterrows():

            report.append(

                f"{row.company_name}"
                f" | Debt={row.debt_to_equity:.2f}"
                f" | Interest={row.interest_coverage:.2f}"

            )

        with open(

            OUTPUT / "analytics_report.txt",

            "w",

            encoding="utf-8"

        ) as f:

            f.write("\n".join(report))

        print()
        print("=" * 80)
        print("Analytics Report Generated")
        print("=" * 80)
        print()