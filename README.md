# 📈 Nifty100 Financial Analytics Platform

A comprehensive financial analytics platform built using Python, SQLite, SQL, and Excel to analyze Nifty 100 companies. The project automates ETL, financial ratio computation, peer comparison, stock screening, and advanced analytics to support investment research and financial decision-making.

---

# 📌 Project Overview

The project is divided into multiple development sprints. The first three sprints establish a complete analytics pipeline starting from raw financial datasets and ending with intelligent stock screening and peer comparison.

---

# 🏗️ Technology Stack

- Python 3.13
- Pandas
- NumPy
- SQLite
- SQL
- Matplotlib
- PyYAML
- OpenPyXL
- Loguru

---

# 📁 Project Structure

```
Nifty100_Project/
│
├── config/
├── data/
│   ├── raw/
│   └── nifty100.db
│
├── notebooks/
│
├── output/
│   ├── radar/
│   ├── screener_output.xlsx
│   ├── peer_percentiles.xlsx
│   └── reports
│
├── src/
│   ├── analysis/
│   ├── analytics/
│   ├── database/
│   ├── etl/
│   ├── screener/
│   └── utils/
│
└── tests/
```

---

# 🚀 Sprint 1 — Data Foundation & ETL

## Objective

Build a robust ETL pipeline capable of importing raw financial datasets into a normalized SQLite database while maintaining data quality.

---

## Features

- Automated Excel Loader
- Data Normalization
- SQLite Database Creation
- Schema Management
- Data Validation
- Data Quality Rules
- Logging
- Database Verification

---

## Modules Developed

```
src/etl/
│
├── loader.py
├── normaliser.py
├── dq_rules.py
├── validator.py

src/database/
│
├── schema.py
├── loader.py
├── sqlite.py
├── verify_database.py
```

---

## Datasets Imported

- Companies
- Balance Sheet
- Profit & Loss
- Cash Flow
- Market Capitalization
- Financial Ratios
- Stock Prices
- Peer Groups
- Sectors
- Documents
- Pros & Cons
- Analysis

---

## Deliverables

- SQLite Database
- ETL Pipeline
- Data Validation
- Data Quality Reports

---

# 📊 Sprint 2 — Financial Ratio Engine

## Objective

Develop a financial analytics engine that computes key financial ratios and quality indicators.

---

## KPIs Implemented

### Profitability

- Net Profit Margin
- Operating Profit Margin
- Return on Equity (ROE)
- Return on Assets (ROA)
- Return on Capital Employed (ROCE)

### Solvency

- Debt to Equity
- Interest Coverage
- Net Debt

### Cash Flow

- Free Cash Flow
- FCF Conversion
- CFO Quality Score

### Valuation

- Earnings Per Share
- Book Value Per Share
- Dividend Payout Ratio

### Growth

- Revenue CAGR
- PAT CAGR
- EPS CAGR

(3-Year, 5-Year and 10-Year calculations)

---

## Additional Analytics

- Composite Quality Score
- High Leverage Detection
- Interest Coverage Warning
- Capex Classification
- Revenue Growth Flags
- EPS Growth Flags

---

## Modules Developed

```
src/analytics/

ratio_engine.py
ratios.py
cashflow_kpis.py
cagr.py
valuation.py
scorecard.py
risk_analysis.py
advanced_analysis.py
report.py
```

---

## Deliverables

- Financial Ratio Engine
- KPI Reports
- Quality Scorecard
- CSV Reports
- SQLite Updates

---

# 📈 Sprint 3 — Stock Screener & Peer Analytics

## Objective

Develop intelligent stock screening and peer comparison tools for investment analysis.

---

## Stock Screener

Implemented a configurable stock screener using YAML-based filtering.

### Screening Parameters

- ROE
- ROCE
- Debt to Equity
- Revenue Growth
- EPS Growth

---

## Composite Stock Score

Ranking based on:

- ROE
- ROCE
- Revenue CAGR
- EPS CAGR

---

## Peer Analytics

Sector-wise comparison including:

- ROE Percentile
- ROCE Percentile
- Net Profit Margin Percentile
- Composite Quality Score Percentile
- Revenue CAGR Percentile
- PAT CAGR Percentile
- EPS CAGR Percentile

---

## Radar Charts

Visual comparison of:

- ROE
- ROCE
- Net Profit Margin
- Composite Quality Score

against sector averages.

---

## Modules Developed

```
src/screener/

engine.py

src/analytics/

peer.py
radar_chart.py
```

---

## Generated Outputs

```
output/

screener_output.xlsx

peer_percentiles.xlsx

peer_comparison.xlsx

radar/

TCS_radar.png
```

---

## SQLite Tables

```
financial_ratios

peer_percentiles
```

---

# 📊 Project Outputs

The project automatically generates:

- Financial Ratio Reports
- Company Rankings
- Sector Analysis
- Peer Percentiles
- Radar Charts
- CSV Reports
- Excel Reports

---

# 🗄️ Database

SQLite Database:

```
data/nifty100.db
```

Contains normalized financial information for all Nifty 100 companies across multiple financial years.

---

# ▶️ Running the Project

## Step 1

Create virtual environment

```bash
python -m venv .venv
```

---

## Step 2

Activate environment

Windows

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
source .venv/bin/activate
```

---

## Step 3

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4

Run ETL

```bash
python -m src.etl.loader
```

---

## Step 5

Generate Financial Ratios

```bash
python -m src.analytics.populate_ratios
```

---

## Step 6

Run Stock Screener

```bash
python -m src.screener.engine
```

---

## Step 7

Generate Peer Analytics

```bash
python -m src.analytics.peer
```

---

## Step 8

Generate Radar Chart

```bash
python -m src.analytics.radar_chart
```

---

# 📊 Project Highlights

✔ Automated ETL Pipeline

✔ SQLite Database

✔ Financial Ratio Engine

✔ CAGR Analytics

✔ Quality Scoring

✔ Risk Analysis

✔ Stock Screener

✔ Peer Comparison

✔ Percentile Engine

✔ Radar Charts

✔ Excel Reporting

✔ Modular Python Architecture

---

# 👨‍💻 Author

**Aarush Singh Nagpal**

B.Tech Electronics & Communication Engineering

Dr. B. R. Ambedkar National Institute of Technology, Jalandhar

---

# 📄 License

This project is developed for educational and analytical purposes.