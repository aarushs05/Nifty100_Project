import sqlite3
import pandas as pd

DB_PATH = "data/nifty100.db"

conn = sqlite3.connect(DB_PATH)


companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

print(companies.head()) 

query = """
SELECT COUNT(*)
FROM companies
"""

print(
    pd.read_sql(query, conn)
)

query = """
SELECT company_id,
       market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10
"""

top_market_cap = pd.read_sql(query, conn)

print(top_market_cap)


query = """
SELECT broad_sector,
       COUNT(*) AS companies
FROM sectors
GROUP BY broad_sector
ORDER BY companies DESC
"""

sector_df = pd.read_sql(query, conn)

print(sector_df)


query = """
SELECT company_id,
       AVG(close_price) AS avg_close
FROM stock_prices
GROUP BY company_id
ORDER BY avg_close DESC
"""

avg_close = pd.read_sql(query, conn)

print(avg_close.head(10))



query = """
SELECT company_id,
       MAX(net_profit) AS max_profit
FROM profitandloss
GROUP BY company_id
ORDER BY max_profit DESC
LIMIT 10
"""

profit = pd.read_sql(query, conn)

print(profit)



top_market_cap.to_csv(
    "output/top_market_cap.csv",
    index=False
)

sector_df.to_csv(
    "output/sector_distribution.csv",
    index=False
)



