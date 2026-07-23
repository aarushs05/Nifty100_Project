"""
Sprint 3 - Advanced Analytics
Main Runner
"""

from src.database.sqlite import SQLiteDB

from src.analytics.scorecard import CompanyScorecard
from src.analytics.sector_analysis import SectorAnalysis
from src.analytics.valuation import ValuationAnalysis
from src.analytics.risk_analysis import RiskAnalysis
from src.analytics.report import AnalyticsReport


class AdvancedAnalytics:

    def __init__(self):

        self.db = SQLiteDB()

        self.ratios = self.db.read_table("financial_ratios")
        self.market = self.db.read_table("market_cap")
        self.company = self.db.read_table("companies")
        self.sector = self.db.read_table("sectors")

    def run(self):

        print("=" * 80)
        print("RUNNING SPRINT 3 ANALYTICS")
        print("=" * 80)

        # --------------------------------------------------
        # Company Scorecard
        # --------------------------------------------------

        scorecard = CompanyScorecard(
            self.ratios,
            self.company,
            self.sector,
            self.market
        ).generate()

        # --------------------------------------------------
        # Sector Analysis
        # --------------------------------------------------

        sector = SectorAnalysis(
            scorecard
        ).generate()

        # --------------------------------------------------
        # Valuation Analysis
        # --------------------------------------------------

        valuation = ValuationAnalysis(
            scorecard
        ).generate()

        # --------------------------------------------------
        # Risk Analysis
        # --------------------------------------------------

        risk = RiskAnalysis(
            scorecard
        ).generate()

        # --------------------------------------------------
        # Final Report
        # --------------------------------------------------

        AnalyticsReport(
            scorecard,
            sector,
            valuation,
            risk
        ).generate()

        self.db.close()

        print()
        print("=" * 80)
        print("SPRINT 3 COMPLETED SUCCESSFULLY")
        print("=" * 80)

        print("\nGenerated Files:")
        print("✔ company_scorecard.csv")
        print("✔ sector_summary.csv")
        print("✔ top_companies.csv")
        print("✔ undervalued_companies.csv")
        print("✔ overvalued_companies.csv")
        print("✔ lowest_risk_companies.csv")
        print("✔ highest_risk_companies.csv")
        print("✔ risk_summary.csv")
        print("✔ analytics_report.txt")


def main():

    analytics = AdvancedAnalytics()
    analytics.run()


if __name__ == "__main__":
    main()