import sqlite3
import pandas as pd
from pathlib import Path

# ----------------------------
# Database Connection
# ----------------------------

DB_PATH = "data/nifty100.db"
OUTPUT_DIR = "output"

Path(OUTPUT_DIR).mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

print("=" * 60)
print("ADVANCED SQL ANALYSIS")
print("=" * 60)

# ----------------------------
# Top Market Cap Companies
# ----------------------------

query = """
SELECT
    company_id,
    ROUND(AVG(market_cap_crore),2) AS avg_market_cap
FROM market_cap
GROUP BY company_id
ORDER BY avg_market_cap DESC
LIMIT 10;
"""

top_market_cap = pd.read_sql(query, conn)

print("\nTop 10 Companies by Average Market Cap")
print(top_market_cap)

# ----------------------------
# Highest ROE Companies
# ----------------------------

query = """
SELECT
    company_name,
    roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;
"""

top_roe = pd.read_sql(query, conn)

print("\nTop 10 ROE Companies")
print(top_roe)

# ----------------------------
# Highest ROCE Companies
# ----------------------------

query = """
SELECT
    company_name,
    roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;
"""

top_roce = pd.read_sql(query, conn)

print("\nTop 10 ROCE Companies")
print(top_roce)

# ----------------------------
# Highest EPS
# ----------------------------

query = """
SELECT
    company_id,
    MAX(earnings_per_share) AS highest_eps
FROM financial_ratios
GROUP BY company_id
ORDER BY highest_eps DESC
LIMIT 10;
"""

top_eps = pd.read_sql(query, conn)

print("\nTop 10 Highest EPS")
print(top_eps)

# ----------------------------
# Average Dividend Yield
# ----------------------------

query = """
SELECT
    ROUND(AVG(dividend_yield_pct),2) AS avg_dividend_yield
FROM market_cap;
"""

dividend_yield = pd.read_sql(query, conn)

print("\nAverage Dividend Yield")
print(dividend_yield)

# ----------------------------
# Highest Trading Volume
# ----------------------------

query = """
SELECT
    company_id,
    SUM(volume) AS total_volume
FROM stock_prices
GROUP BY company_id
ORDER BY total_volume DESC
LIMIT 10;
"""

top_volume = pd.read_sql(query, conn)

print("\nTop 10 Highest Trading Volume")
print(top_volume)

# ----------------------------
# Average Profit
# ----------------------------

query = """
SELECT
    company_id,
    AVG(net_profit) AS average_profit
FROM profitandloss
GROUP BY company_id
ORDER BY average_profit DESC
LIMIT 10;
"""

top_profit = pd.read_sql(query, conn)

print("\nTop 10 Average Profit")
print(top_profit)

# ----------------------------
# Export Reports
# ----------------------------

top_market_cap.to_csv(
    f"{OUTPUT_DIR}/top_market_cap.csv",
    index=False
)

top_roe.to_csv(
    f"{OUTPUT_DIR}/top_roe.csv",
    index=False
)

top_roce.to_csv(
    f"{OUTPUT_DIR}/top_roce.csv",
    index=False
)

top_eps.to_csv(
    f"{OUTPUT_DIR}/top_eps.csv",
    index=False
)

dividend_yield.to_csv(
    f"{OUTPUT_DIR}/average_dividend_yield.csv",
    index=False
)

top_volume.to_csv(
    f"{OUTPUT_DIR}/top_volume.csv",
    index=False
)

top_profit.to_csv(
    f"{OUTPUT_DIR}/top_profit.csv",
    index=False
)

conn.close()

print("\n" + "=" * 60)
print("Analysis Complete!")
print("CSV reports saved to the output/ folder.")
print("=" * 60)