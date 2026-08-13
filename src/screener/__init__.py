"""Screener package."""

from src.database.sqlite import SQLiteDB


class AdvancedAnalytics:
    """Provide access to database tables for advanced analytics."""

    def __init__(self):
        """Load required analytics tables from SQLite."""

        self.db = SQLiteDB()

        self.ratios = self.db.read_table("financial_ratios")
        self.market = self.db.read_table("market_cap")
        self.company = self.db.read_table("companies")
        self.sector = self.db.read_table("sectors")

        print("financial_ratios:", self.ratios.shape)
        print("market_cap:", self.market.shape)
        print("companies:", self.company.shape)
        print("sectors:", self.sector.shape)

    def run(self):
        """Run advanced analytics."""
        return