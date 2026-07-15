# Sprint 2 – Financial Ratio Engine

## Overview

Sprint 2 focuses on building a Financial Ratio Engine capable of computing key financial KPIs for all companies and years available in the SQLite database. The engine integrates data from the Profit & Loss, Balance Sheet, Cash Flow, Companies, and Sectors tables to generate a consolidated `financial_ratios` table.

The solution computes profitability, leverage, efficiency, cash flow, and growth metrics while handling common financial edge cases. The generated data is stored in SQLite and used for further analytics.

---

# Sprint Goal

Develop a reusable analytics engine that:

- Computes financial KPIs for every company-year.
- Populates the `financial_ratios` table.
- Generates capital allocation classifications.
- Supports CAGR calculations with edge-case handling.
- Produces structured outputs suitable for dashboards and further analysis.

---

# Project Structure

```
src/
│
├── analytics/
│   ├── ratios.py
│   ├── cagr.py
│   ├── cashflow_kpis.py
│   ├── ratio_engine.py
│   └── populate_ratios.py
│
├── database/
│   └── sqlite.py
│
tests/
└── kpi/
```

---

# Modules

## ratios.py

Contains implementations for profitability, leverage, and efficiency ratios.

Implemented metrics:

- Net Profit Margin
- Operating Profit Margin
- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Return on Assets (ROA)
- Debt to Equity Ratio
- Interest Coverage Ratio
- Net Debt
- Asset Turnover
- Composite Quality Score

Additional functionality:

- High Leverage Flag
- Interest Coverage Warning Flag
- Debt Free Label
- ROE Cross-check
- ROCE Cross-check
- OPM Cross-check

---

## cagr.py

Implements CAGR calculations for multiple financial metrics.

Supported CAGR windows:

- 3 Year
- 5 Year
- 10 Year

Supported metrics:

- Revenue CAGR
- PAT CAGR
- EPS CAGR

Edge cases handled:

- Zero Base
- Turnaround
- Decline to Loss
- Both Negative
- Insufficient Data

Each CAGR value is stored together with an associated flag.

---

## cashflow_kpis.py

Computes cash flow related KPIs.

Implemented metrics:

- Free Cash Flow
- CFO / PAT Ratio
- CFO Quality Score
- CapEx Intensity
- FCF Conversion
- Capital Allocation Classification

Capital allocation patterns:

- Reinvestor
- Shareholder Returns
- Liquidating Assets
- Distress Signal
- Growth Funded by Debt
- Cash Accumulator
- Pre-Revenue
- Mixed

---

## sqlite.py

Provides helper functions for interacting with SQLite.

Features:

- Database connection
- Read tables
- Replace table
- Append table
- Execute SQL
- Fetch records
- Row count verification

---

## ratio_engine.py

Core analytics engine.

Responsibilities:

- Load source tables
- Clean financial data
- Merge datasets
- Compute all KPIs
- Compute CAGR metrics
- Generate capital allocation records
- Return consolidated dataframe

Source tables used:

- profitandloss
- balancesheet
- cashflow
- companies
- sectors

---

## populate_ratios.py

Main execution script.

Responsibilities:

- Run Ratio Engine
- Populate financial_ratios table
- Generate capital_allocation.csv
- Generate ratio_edge_cases.log
- Verify database row count

Execution command:

```bash
python -m src.analytics.populate_ratios
```

---

# Financial Ratios Implemented

## Profitability

- Net Profit Margin
- Operating Profit Margin
- Return on Equity
- Return on Capital Employed
- Return on Assets

---

## Leverage

- Debt to Equity
- Interest Coverage Ratio
- Net Debt

---

## Efficiency

- Asset Turnover

---

## Cash Flow

- Free Cash Flow
- FCF Conversion
- CFO Quality
- CapEx Intensity

---

## Growth

- Revenue CAGR
- PAT CAGR
- EPS CAGR

---

## Quality Metrics

- Composite Quality Score

---

# Database Output

The generated `financial_ratios` table contains the following KPI columns:

- company_id
- year
- net_profit_margin_pct
- operating_profit_margin_pct
- return_on_equity_pct
- return_on_assets_pct
- return_on_capital_employed_pct
- debt_to_equity
- interest_coverage
- interest_coverage_label
- interest_warning_flag
- high_leverage_flag
- asset_turnover
- net_debt
- free_cash_flow_cr
- fcf_conversion_pct
- capex_intensity_pct
- capex_category
- cfo_quality_score
- cfo_quality_label
- earnings_per_share
- book_value_per_share
- dividend_payout_ratio_pct
- total_debt_cr
- cash_from_operations_cr
- composite_quality_score
- Revenue CAGR (3/5/10 Year)
- PAT CAGR (3/5/10 Year)
- EPS CAGR (3/5/10 Year)
- CAGR Flags

---

# Output Files

Generated automatically:

```
output/

capital_allocation.csv

ratio_edge_cases.log
```

---

# Database Summary

SQLite Database:

```
data/nifty100.db
```

Tables used:

- analysis
- balancesheet
- cashflow
- companies
- documents
- financial_ratios
- market_cap
- peer_groups
- profitandloss
- prosandcons
- sectors
- stock_prices

---

# Execution Flow

1. Read financial tables from SQLite
2. Clean year fields
3. Merge source tables
4. Compute profitability ratios
5. Compute leverage ratios
6. Compute efficiency ratios
7. Compute cash flow KPIs
8. Compute CAGR metrics
9. Generate quality score
10. Store results into SQLite
11. Export capital allocation CSV
12. Generate log file

---

# Result

Successful execution generated:

- Financial Ratios Table
- 44 KPI Columns
- 1263 Company-Year Records
- Capital Allocation CSV
- Ratio Edge Case Log

---

# Technologies Used

- Python 3.13
- Pandas
- SQLite3
- NumPy
- Logging
- Pathlib

---

# Sprint Outcome

Sprint 2 successfully delivers a reusable financial ratio engine capable of computing financial KPIs from structured financial statements. The generated dataset is stored in SQLite for downstream analytics, dashboards, and screening applications.