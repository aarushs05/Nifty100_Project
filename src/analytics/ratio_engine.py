"""
Financial Ratio Engine

Reads all financial tables,
computes KPIs,
returns a dataframe ready for SQLite.
"""

from __future__ import annotations

import logging

import pandas as pd

from src.database.sqlite import SQLiteDB

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
    net_debt,
    quality_score,
    high_leverage_flag,
    icr_label,
    icr_warning_flag,
    check_opm_difference,
    check_roce_difference,
    check_roe_difference,
    ebit
)

from src.analytics.cashflow_kpis import (
    compute_cashflow_metrics
)

from src.analytics.cagr import (
    compute_all_cagr,
    cagr_to_record
)

logger = logging.getLogger(__name__)


class RatioEngine:

    def __init__(self):

        self.db = SQLiteDB()

        self.pnl = self.db.table(
            "profitandloss"
        )

        self.bs = self.db.table(
            "balancesheet"
        )

        self.cf = self.db.table(
            "cashflow"
        )

        self.company = self.db.table(
            "companies"
        )

        self.sector = self.db.table(
            "sectors"
        )

        self.results = []

        self.capital_records = []
        self.pnl = self.pnl.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

        self.bs = self.bs.drop_duplicates(
        subset=["company_id", "year"],
        keep="first"
)

        self.cf = self.cf.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)   
    # ======================================================
    # Merge Tables
    # ======================================================

    def merged_dataframe(self):

    # Remove TTM
        self.pnl = self.pnl[self.pnl["year"] != "TTM"].copy()

        self.pnl["year"] = pd.to_numeric(
        self.pnl["year"],
        errors="coerce"
    )

        self.pnl = self.pnl.dropna(subset=["year"])

        self.pnl["year"] = self.pnl["year"].astype(int)
        self.bs["year"] = self.bs["year"].astype(int)
        self.cf["year"] = self.cf["year"].astype(int)

    # Keep only required columns
        pnl = self.pnl[
        [
            "company_id",
            "year",
            "sales",
            "operating_profit",
            "opm_percentage",
            "other_income",
            "interest",
            "net_profit",
            "eps",
            "dividend_payout"
        ]
    ]

        bs = self.bs[
        [
            "company_id",
            "year",
            "equity_capital",
            "reserves",
            "borrowings",
            "investments",
            "total_assets"
        ]
    ]

        cf = self.cf[
        [
            "company_id",
            "year",
            "operating_activity",
            "investing_activity",
            "financing_activity"
        ]
    ]

        company = self.company[
        [
            "id",
            "book_value",
            "roce_percentage",
            "roe_percentage"
        ]
        ]

        sector = self.sector[
        [
            "company_id",
            "broad_sector"
        ]
        ]

        df = pnl.merge(bs, on=["company_id", "year"])
        df = df.merge(cf, on=["company_id", "year"])
        df = df.merge(company, left_on="company_id", right_on="id")
        df = df.drop(columns=["id"])
        df = df.merge(sector, on="company_id")

        return df
    # ======================================================
    # Compute Ratios
    # ======================================================

    def compute(self):

        df = self.merged_dataframe()

        for _, row in df.iterrows():

            company = row.company_id

            year = int(row.year)

            npm = net_profit_margin(

                row.net_profit,

                row.sales

            )

            opm = operating_profit_margin(

                row.operating_profit,

                row.sales

            )

            check_opm_difference(

                opm,

                row.opm_percentage,

                company,

                year

            )

            EBIT = ebit(

                row.operating_profit,

                row.other_income

            )

            roe = return_on_equity(

                row.net_profit,

                row.equity_capital,

                row.reserves

            )

            roce = return_on_capital_employed(

                EBIT,

                row.equity_capital,

                row.reserves,

                row.borrowings

            )

            roa = return_on_assets(

                row.net_profit,

                row.total_assets

            )
            de = debt_to_equity(
                row.borrowings,
                row.equity_capital,
                row.reserves
            )

            leverage_flag = high_leverage_flag(
                de,
                row.broad_sector
            )

            icr = interest_coverage_ratio(
                row.operating_profit,
                row.other_income,
                row.interest
            )

            icr_text = icr_label(
                row.interest,
                icr
            )

            icr_flag = icr_warning_flag(
                icr
            )

            debt = net_debt(
                row.borrowings,
                row.investments
            )

            turnover = asset_turnover(
                row.sales,
                row.total_assets
            )

            check_roce_difference(
                roce,
                row.roce_percentage,
                company,
                year
            )

            check_roe_difference(
                roe,
                row.roe_percentage,
                company,
                year
            )

            cash_metrics = compute_cashflow_metrics(

                operating_activity=row.operating_activity,

                investing_activity=row.investing_activity,

                financing_activity=row.financing_activity,

                sales=row.sales,

                operating_profit=row.operating_profit,

                net_profit=row.net_profit,

                quality_history=[]
            )

            self.capital_records.append({

                "company_id": company,

                "year": year,

                "cfo_sign":
                    cash_metrics["cfo_sign"],

                "cfi_sign":
                    cash_metrics["cfi_sign"],

                "cff_sign":
                    cash_metrics["cff_sign"],

                "pattern_label":
                    cash_metrics["pattern_label"]

            })

            score = quality_score(

                roe,

                roce,

                npm,

                de

            )

            record = {

                "company_id": company,

                "year": year,

                "net_profit_margin_pct": npm,

                "operating_profit_margin_pct": opm,

                "return_on_equity_pct": roe,

                "return_on_assets_pct": roa,

                "return_on_capital_employed_pct": roce,

                "debt_to_equity": de,

                "interest_coverage": icr,

                "interest_coverage_label": icr_text,

                "interest_warning_flag": icr_flag,

                "high_leverage_flag": leverage_flag,

                "asset_turnover": turnover,

                "net_debt": debt,

                "free_cash_flow_cr":
                    cash_metrics["free_cash_flow"],

                "fcf_conversion_pct":
                    cash_metrics["fcf_conversion"],

                "capex_intensity_pct":
                    cash_metrics["capex_intensity"],

                "capex_category":
                    cash_metrics["capex_label"],

                "cfo_quality_score":
                    cash_metrics["cfo_quality_score"],

                "cfo_quality_label":
                    cash_metrics["cfo_quality_label"],

                "earnings_per_share":
                    row.eps,

                "book_value_per_share":
                    row.book_value,

                "dividend_payout_ratio_pct":
                    row.dividend_payout,

                "total_debt_cr":
                    row.borrowings,

                "cash_from_operations_cr":
                    row.operating_activity,

                "composite_quality_score":
                    score

            }

            self.results.append(record)

        return pd.DataFrame(
            self.results
        )
    
    # ======================================================
    # Compute CAGR
    # ======================================================

    def compute_cagr(self):

        pnl = self.pnl.copy()

        pnl["year"] = pnl["year"].astype(int)

        cagr_records = []

        for company in pnl["company_id"].unique():

            company_df = (
                pnl[pnl["company_id"] == company]
                .sort_values("year")
            )

            revenue = company_df["sales"].tolist()
            pat = company_df["net_profit"].tolist()
            eps = company_df["eps"].tolist()

            result = compute_all_cagr(
                revenue,
                pat,
                eps
            )

            latest_year = company_df.iloc[-1]["year"]

            record = {
                "company_id": company,
                "year": latest_year
            }

            record.update(
                cagr_to_record(result)
            )

            cagr_records.append(record)

        return pd.DataFrame(cagr_records)

    # ======================================================
    # Run Engine
    # ======================================================

    def run(self):

        ratios = self.compute()

        cagr = self.compute_cagr()

        final = ratios.merge(
            cagr,
            on=["company_id", "year"],
            how="left"
        )

        return final


# ======================================================
# Main
# ======================================================

if __name__ == "__main__":

    engine = RatioEngine()

    df = engine.run()

    print(df.head())

    print()

    print(
        f"Total Rows : {len(df)}"
    )

    print()

    print(df.columns)

    engine.db.close()


# import sqlite3

# conn = sqlite3.connect("data/nifty100.db")

# cursor = conn.cursor()

# cursor.execute("PRAGMA table_info(financial_ratios)")

# for row in cursor.fetchall():
#     print(row)

# conn.close()

# import sqlite3
# import pandas as pd

# conn = sqlite3.connect("data/nifty100.db")

# df = pd.read_sql(
#     "SELECT * FROM financial_ratios LIMIT 5",
#     conn
# )

# print(df)

# conn.close()