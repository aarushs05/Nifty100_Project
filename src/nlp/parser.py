import re
import sqlite3
import pandas as pd
from pathlib import Path

PATTERN = r"(\d+)\s*Years?\s*:?\s*([\d.]+)%"

DB_PATH = "data/nifty100.db"

conn = sqlite3.connect(DB_PATH)

analysis_df = pd.read_sql(
    "SELECT * FROM analysis",
    conn
)

parsed_rows = []
failures = []

TARGET_COLUMNS = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

for _, row in analysis_df.iterrows():

    company_id = row["company_id"]

    for metric in TARGET_COLUMNS:

        text = str(row[metric])

        matches = re.findall(PATTERN, text)

        if matches:

            for period, value in matches:

                parsed_rows.append({
                    "company_id": company_id,
                    "metric_type": metric,
                    "period_years": int(period),
                    "value_pct": float(value)
                })

        else:

            failures.append({
                "company_id": company_id,
                "metric_type": metric,
                "raw_text": text
            })

parsed_df = pd.DataFrame(parsed_rows)
failure_df = pd.DataFrame(failures)

Path("output").mkdir(exist_ok=True)

parsed_df.to_csv(
    "output/analysis_parsed.csv",
    index=False
)

failure_df.to_csv(
    "output/parse_failures.csv",
    index=False
)

print(f"Parsed rows : {len(parsed_df)}")
print(f"Failures    : {len(failure_df)}")