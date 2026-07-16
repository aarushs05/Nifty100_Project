"""
Populate financial_ratios table
Generate capital allocation CSV
"""

from pathlib import Path
import logging

import pandas as pd

from src.analytics.ratio_engine import RatioEngine
from src.database.sqlite import SQLiteDB

logging.basicConfig(
    filename="output/ratio_edge_cases.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

ROOT = Path(__file__).resolve().parents[2]

OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)


def populate():

    db = SQLiteDB()

    engine = RatioEngine()

    print("Running Ratio Engine...")

    ratios = engine.run()

    print(f"Computed {len(ratios)} rows")

    # -----------------------------------
    # Replace financial_ratios table
    # -----------------------------------

    db.replace_table(
        ratios,
        "financial_ratios"
    )

    print("financial_ratios updated")

    # -----------------------------------
    # Capital Allocation CSV
    # -----------------------------------

    capital = pd.DataFrame(
        engine.capital_records
    )

    capital.to_csv(

        OUTPUT /
        "capital_allocation.csv",

        index=False

    )

    print("capital_allocation.csv created")

    # -----------------------------------
    # Verification
    # -----------------------------------

    rows = db.row_count(
        "financial_ratios"
    )

    print()

    print("=" * 50)

    print(
        f"financial_ratios rows : {rows}"
    )

    if rows >= 1100:

        print("PASS ✓")

    else:

        print("WARNING : Row count below target")

    print("=" * 50)

    db.close()


if __name__ == "__main__":

    populate()




# import sqlite3
# import pandas as pd

# conn = sqlite3.connect("data/nifty100.db")

# df = pd.read_sql("""
# SELECT *
# FROM profitandloss
# WHERE company_id='ADANIPORTS'
# AND year='2014'
# """, conn)

# print(df)

# conn.close()

# import sqlite3
# import pandas as pd

# conn = sqlite3.connect("data/nifty100.db")

# df = pd.read_sql("""
# SELECT *
# FROM cashflow
# WHERE company_id='ABB'
# AND year=2014
# """, conn)

# print(df)

# conn.close()


# import sqlite3
# import pandas as pd

# conn = sqlite3.connect("data/nifty100.db")

# df = pd.read_sql("""
# SELECT *
# FROM documents
# WHERE company_id='ABB'
# """, conn)

# print(df)

# conn.close()
