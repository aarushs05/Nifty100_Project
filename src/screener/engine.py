import sqlite3
from pathlib import Path

import pandas as pd
import yaml

DB = "data/nifty100.db"
CONFIG = "config/screener_config.yaml"

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)


def load_config():
    with open(CONFIG, "r") as f:
        return yaml.safe_load(f)


def load_data():
    conn = sqlite3.connect(DB)

    query = """
    SELECT

        fr.company_id,
        fr.year,

        c.company_name,

        s.broad_sector,
        s.sub_sector,

        mc.market_cap_crore,
        mc.pe_ratio,
        mc.pb_ratio,
        mc.dividend_yield_pct,

        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.debt_to_equity,
        fr.net_profit_margin_pct,
        fr.composite_quality_score,

        fr.revenue_cagr_3yr,
        fr.eps_cagr_3yr

    FROM financial_ratios fr

    LEFT JOIN companies c
        ON fr.company_id = c.id

    LEFT JOIN sectors s
        ON fr.company_id = s.company_id

    LEFT JOIN market_cap mc
        ON fr.company_id = mc.company_id
       AND fr.year = mc.year
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def apply_filters(df, cfg):

    f = cfg["filters"]

    df = df[
        df["return_on_equity_pct"] >= f["roe"]["min"]
    ]

    df = df[
        df["return_on_capital_employed_pct"] >= f["roce"]["min"]
    ]

    df = df[
        (df["broad_sector"] == "Financial")
        | (df["debt_to_equity"] <= f["debt_to_equity"]["max"])
    ]

    return df


def calculate_score(df):

    df = df.copy()

    df["score"] = (

        df["return_on_equity_pct"] * 0.30

        + df["return_on_capital_employed_pct"] * 0.30

        + df["revenue_cagr_3yr"].fillna(0) * 0.20

        + df["eps_cagr_3yr"].fillna(0) * 0.20

    )

    return df.sort_values(
        "score",
        ascending=False
    )


def main():

    cfg = load_config()

    df = load_data()

    print(f"\nLoaded {len(df)} rows")

    screened = apply_filters(df, cfg)

    ranked = calculate_score(screened)

    ranked.to_excel(
        OUTPUT / "screener_output.xlsx",
        index=False
    )

    print("\nTop 20 Stocks\n")

    print(
        ranked[
            [
                "company_id",
                "company_name",
                "score",
                "return_on_equity_pct",
                "return_on_capital_employed_pct",
            ]
        ].head(20)
    )


if __name__ == "__main__":
    main()