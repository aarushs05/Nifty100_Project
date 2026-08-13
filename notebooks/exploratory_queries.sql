-- ============================================================
-- Nifty100 Financial Analytics
-- Exploratory SQL Queries
-- Sprint 1 - D-04
-- ============================================================

-- ------------------------------------------------------------
-- 1. List all companies
-- ------------------------------------------------------------

SELECT
    id AS company_id,
    company_name
FROM companies
ORDER BY company_name;


-- ------------------------------------------------------------
-- 2. Count companies
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS total_companies
FROM companies;


-- ------------------------------------------------------------
-- 3. Companies by sector
-- ------------------------------------------------------------

SELECT
    broad_sector,
    COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;


-- ------------------------------------------------------------
-- 4. Companies by market-cap category
-- ------------------------------------------------------------

SELECT
    market_cap_category,
    COUNT(*) AS company_count
FROM sectors
GROUP BY market_cap_category
ORDER BY company_count DESC;


-- ------------------------------------------------------------
-- 5. Financial ratio coverage by year
-- ------------------------------------------------------------

SELECT
    year,
    COUNT(DISTINCT company_id) AS companies,
    COUNT(*) AS ratio_rows
FROM financial_ratios
GROUP BY year
ORDER BY year;


-- ------------------------------------------------------------
-- 6. Latest financial ratio record for each company
-- ------------------------------------------------------------

SELECT
    fr.company_id,
    c.company_name,
    fr.year,
    fr.return_on_equity_pct,
    fr.return_on_capital_employed_pct,
    fr.debt_to_equity,
    fr.free_cash_flow_cr,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.composite_quality_score
FROM financial_ratios fr
JOIN companies c
    ON c.id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
ORDER BY fr.composite_quality_score DESC;


-- ------------------------------------------------------------
-- 7. Top 10 companies by ROE
-- ------------------------------------------------------------

SELECT
    fr.company_id,
    c.company_name,
    fr.year,
    fr.return_on_equity_pct AS roe_pct
FROM financial_ratios fr
JOIN companies c
    ON c.id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
AND fr.return_on_equity_pct IS NOT NULL
ORDER BY fr.return_on_equity_pct DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 8. Top 10 companies by ROCE
-- ------------------------------------------------------------

SELECT
    fr.company_id,
    c.company_name,
    fr.year,
    fr.return_on_capital_employed_pct AS roce_pct
FROM financial_ratios fr
JOIN companies c
    ON c.id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
AND fr.return_on_capital_employed_pct IS NOT NULL
ORDER BY fr.return_on_capital_employed_pct DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 9. Lowest debt-to-equity companies
-- ------------------------------------------------------------

SELECT
    fr.company_id,
    c.company_name,
    fr.year,
    fr.debt_to_equity
FROM financial_ratios fr
JOIN companies c
    ON c.id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
AND fr.debt_to_equity IS NOT NULL
ORDER BY fr.debt_to_equity ASC
LIMIT 10;


-- ------------------------------------------------------------
-- 10. Top companies by free cash flow
-- ------------------------------------------------------------

SELECT
    fr.company_id,
    c.company_name,
    fr.year,
    fr.free_cash_flow_cr
FROM financial_ratios fr
JOIN companies c
    ON c.id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
AND fr.free_cash_flow_cr IS NOT NULL
ORDER BY fr.free_cash_flow_cr DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 11. Top companies by 5-year revenue CAGR
-- ------------------------------------------------------------

SELECT
    fr.company_id,
    c.company_name,
    fr.revenue_cagr_5yr
FROM financial_ratios fr
JOIN companies c
    ON c.id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
AND fr.revenue_cagr_5yr IS NOT NULL
ORDER BY fr.revenue_cagr_5yr DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 12. Top companies by 5-year PAT CAGR
-- ------------------------------------------------------------

SELECT
    fr.company_id,
    c.company_name,
    fr.pat_cagr_5yr
FROM financial_ratios fr
JOIN companies c
    ON c.id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
AND fr.pat_cagr_5yr IS NOT NULL
ORDER BY fr.pat_cagr_5yr DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 13. Top 10 companies by composite quality score
-- ------------------------------------------------------------

SELECT
    fr.company_id,
    c.company_name,
    s.broad_sector,
    fr.composite_quality_score
FROM financial_ratios fr
JOIN companies c
    ON c.id = fr.company_id
LEFT JOIN sectors s
    ON s.company_id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
AND fr.composite_quality_score IS NOT NULL
ORDER BY fr.composite_quality_score DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 14. Sector-level average ROE
-- ------------------------------------------------------------

SELECT
    s.broad_sector,
    COUNT(DISTINCT fr.company_id) AS companies,
    ROUND(AVG(fr.return_on_equity_pct), 2) AS avg_roe_pct
FROM financial_ratios fr
JOIN sectors s
    ON s.company_id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
GROUP BY s.broad_sector
ORDER BY avg_roe_pct DESC;


-- ------------------------------------------------------------
-- 15. Sector-level average ROCE
-- ------------------------------------------------------------

SELECT
    s.broad_sector,
    COUNT(DISTINCT fr.company_id) AS companies,
    ROUND(AVG(fr.return_on_capital_employed_pct), 2) AS avg_roce_pct
FROM financial_ratios fr
JOIN sectors s
    ON s.company_id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
GROUP BY s.broad_sector
ORDER BY avg_roce_pct DESC;


-- ------------------------------------------------------------
-- 16. Sector-level average debt-to-equity
-- ------------------------------------------------------------

SELECT
    s.broad_sector,
    COUNT(DISTINCT fr.company_id) AS companies,
    ROUND(AVG(fr.debt_to_equity), 2) AS avg_debt_to_equity
FROM financial_ratios fr
JOIN sectors s
    ON s.company_id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
GROUP BY s.broad_sector
ORDER BY avg_debt_to_equity ASC;


-- ------------------------------------------------------------
-- 17. Market-cap overview
-- ------------------------------------------------------------

SELECT
    year,
    COUNT(*) AS records,
    ROUND(SUM(market_cap_cr), 2) AS total_market_cap_cr,
    ROUND(AVG(market_cap_cr), 2) AS average_market_cap_cr
FROM market_cap
GROUP BY year
ORDER BY year;


-- ------------------------------------------------------------
-- 18. Stock-price coverage
-- ------------------------------------------------------------

SELECT
    company_id,
    COUNT(*) AS price_records,
    MIN(date) AS first_date,
    MAX(date) AS last_date
FROM stock_prices
GROUP BY company_id
ORDER BY company_id;


-- ------------------------------------------------------------
-- 19. Peer-group sizes
-- ------------------------------------------------------------

SELECT
    peer_group_name,
    COUNT(*) AS company_count
FROM peer_groups
GROUP BY peer_group_name
ORDER BY company_count DESC;


-- ------------------------------------------------------------
-- 20. Peer percentile overview
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS total_peer_percentile_rows,
    COUNT(DISTINCT company_id) AS companies
FROM peer_percentiles;


-- ------------------------------------------------------------
-- 21. Financial statement coverage
-- ------------------------------------------------------------

SELECT
    'profitandloss' AS table_name,
    COUNT(*) AS rows
FROM profitandloss

UNION ALL

SELECT
    'balancesheet',
    COUNT(*)
FROM balancesheet

UNION ALL

SELECT
    'cashflow',
    COUNT(*)
FROM cashflow

UNION ALL

SELECT
    'analysis',
    COUNT(*)
FROM analysis;


-- ------------------------------------------------------------
-- 22. Annual report/document coverage
-- ------------------------------------------------------------

SELECT
    company_id,
    COUNT(*) AS document_count,
    MIN(year) AS earliest_year,
    MAX(year) AS latest_year
FROM documents
GROUP BY company_id
ORDER BY document_count DESC;


-- ------------------------------------------------------------
-- 23. Companies with highest quality score and strong ROE
-- ------------------------------------------------------------

SELECT
    fr.company_id,
    c.company_name,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.free_cash_flow_cr,
    fr.composite_quality_score
FROM financial_ratios fr
JOIN companies c
    ON c.id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
AND fr.return_on_equity_pct >= 15
AND fr.composite_quality_score >= 50
ORDER BY fr.composite_quality_score DESC;


-- ------------------------------------------------------------
-- 24. Low leverage + positive free cash flow
-- ------------------------------------------------------------

SELECT
    fr.company_id,
    c.company_name,
    fr.debt_to_equity,
    fr.free_cash_flow_cr,
    fr.composite_quality_score
FROM financial_ratios fr
JOIN companies c
    ON c.id = fr.company_id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
AND fr.debt_to_equity <= 1
AND fr.free_cash_flow_cr > 0
ORDER BY fr.composite_quality_score DESC;


-- ============================================================
-- END OF EXPLORATORY QUERIES
-- ============================================================
