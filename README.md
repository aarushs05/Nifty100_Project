# Nifty100 Financial Analytics

## Sprint 1 – Data Foundation

### Project Overview
This project builds an ETL pipeline for the Nifty100 financial dataset. The pipeline reads 12 Excel datasets, normalizes the data, validates quality rules, and loads the cleaned data into a SQLite database.

---

## Technology Stack

- Python 3.13
- Pandas
- SQLite
- SQLAlchemy
- Pytest
- OpenPyXL
- Loguru

---

## Sprint 1 Progress

### ✅ Day 1 – Environment Setup

- Project folder structure created
- Virtual environment configured
- Required libraries installed
- Dataset organized
- Configuration files created
- Git initialized

---

### ✅ Day 2 – Excel Loader & Normalisation

Implemented:

- Automatic detection of all Excel files
- Support for report-style Excel sheets
- Automatic header detection
- Data loading using Pandas
- Company ID normalization
- Year normalization
- Text normalization
- Logging using Loguru
- Initial Pytest unit tests

---

## Project Structure

```text
Nifty100_Project/

├── config/
├── data/
│   ├── raw/
│   └── processed/
├── db/
├── docs/
├── logs/
├── notebooks/
├── output/
├── src/
│   ├── etl/
│   ├── database/
│   └── utils/
├── tests/
│   └── etl/
├── .env
├── requirements.txt
└── README.md
```

---

## Next Milestone

Sprint 1 – Day 3

- Data Quality Validation
- DQ-01 to DQ-16
- validation_failures.csv
- SQLite schema