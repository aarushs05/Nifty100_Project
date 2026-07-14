import sqlite3
import sys
from pathlib import Path

import pandas as pd

# Add project src directory to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from etl.loader import ExcelLoader


DB_PATH = "data/nifty100.db"


def load_database():

    print("=" * 60)
    print("LOADING SQLITE DATABASE")
    print("=" * 60)

    loader = ExcelLoader()
    datasets = loader.load_all()

    conn = sqlite3.connect(DB_PATH)

    total_tables = 0

    for filename, df in datasets.items():

        table_name = filename.replace(".xlsx", "")

        print(f"Loading {table_name:<20} {len(df):>6} rows")

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False,
        )

        total_tables += 1

    conn.commit()
    conn.close()

    print("\n" + "=" * 60)
    print("DATABASE LOAD COMPLETE")
    print("=" * 60)
    print(f"Tables Loaded : {total_tables}")
    print(f"Database      : {DB_PATH}")


if __name__ == "__main__":
    load_database()