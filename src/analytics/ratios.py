"""
Financial Ratio Engine
Sprint 2 - Profitability, Leverage & Efficiency Ratios

Author: Aarush Singh
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)


# ============================================================
# Helper Functions
# ============================================================

def safe_divide(numerator: float,
                denominator: float) -> Optional[float]:
    """
    Safe division.

    Returns None when denominator is zero.
    """

    if denominator == 0:
        return None

    return numerator / denominator


def round_ratio(value: Optional[float],
                digits: int = 2) -> Optional[float]:

    if value is None:
        return None

    return round(value, digits)


# ============================================================
# Profitability Ratios
# ============================================================

def net_profit_margin(
        net_profit: float,
        sales: float
) -> Optional[float]:
    """
    Net Profit Margin

    Formula

    Net Profit / Sales × 100
    """

    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(
        operating_profit: float,
        sales: float
) -> Optional[float]:
    """
    Operating Profit Margin
    """

    if sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def check_opm_difference(
        calculated_opm: Optional[float],
        source_opm: Optional[float],
        company: str,
        year: int
) -> bool:
    """
    Cross-check calculated OPM against source.

    Returns True if mismatch >1%.
    """

    if calculated_opm is None:
        return False

    if source_opm is None:
        return False

    diff = abs(calculated_opm - source_opm)

    if diff > 1:

        logger.warning(
            f"{company}-{year} "
            f"OPM mismatch "
            f"Calculated={calculated_opm} "
            f"Source={source_opm}"
        )

        return True

    return False


def return_on_equity(
        net_profit: float,
        equity_capital: float,
        reserves: float
) -> Optional[float]:
    """
    ROE

    Net Profit /
    (Equity Capital + Reserves)

    ×100
    """

    shareholder_equity = (
        equity_capital +
        reserves
    )

    if shareholder_equity <= 0:
        return None

    return round(
        (
            net_profit /
            shareholder_equity
        ) * 100,
        2
    )


def return_on_capital_employed(
        ebit: float,
        equity_capital: float,
        reserves: float,
        borrowings: float
) -> Optional[float]:
    """
    ROCE

    EBIT /

    (Equity + Reserves + Borrowings)

    ×100
    """

    capital_employed = (
        equity_capital +
        reserves +
        borrowings
    )

    if capital_employed <= 0:
        return None

    return round(
        (
            ebit /
            capital_employed
        ) * 100,
        2
    )


def return_on_assets(
        net_profit: float,
        total_assets: float
) -> Optional[float]:
    """
    ROA
    """

    if total_assets == 0:
        return None

    return round(
        (
            net_profit /
            total_assets
        ) * 100,
        2
    )


# ============================================================
# Leverage Ratios
# ============================================================

def debt_to_equity(
        borrowings: float,
        equity_capital: float,
        reserves: float
) -> Optional[float]:
    """
    Debt / Equity

    Debt Free

    return 0
    """

    if borrowings == 0:
        return 0

    shareholder_equity = (
        equity_capital +
        reserves
    )

    if shareholder_equity <= 0:
        return None

    return round(
        borrowings /
        shareholder_equity,
        2
    )


def high_leverage_flag(
        debt_equity: Optional[float],
        broad_sector: str
) -> bool:
    """
    High leverage

    Ignore Financials
    """

    if debt_equity is None:
        return False

    if broad_sector.lower() == "financials":
        return False

    return debt_equity > 5


# ============================================================
# Interest Coverage Ratio
# ============================================================

def interest_coverage_ratio(
        operating_profit: float,
        other_income: float,
        interest: float
) -> Optional[float]:
    """
    Interest Coverage Ratio

    (Operating Profit + Other Income)
    ---------------------------------
            Interest
    """

    if interest == 0:
        return None

    icr = (
        operating_profit +
        other_income
    ) / interest

    return round(icr, 2)


def icr_label(
        interest: float,
        icr: Optional[float]
) -> str:
    """
    Display label
    """

    if interest == 0:
        return "Debt Free"

    if icr is None:
        return "N/A"

    return ""


def icr_warning_flag(
        icr: Optional[float]
) -> bool:
    """
    Company unable to comfortably
    pay interest.
    """

    if icr is None:
        return False

    return icr < 1.5


# ============================================================
# Net Debt
# ============================================================

def net_debt(
        borrowings: float,
        investments: float
) -> float:
    """
    Net Debt

    Borrowings -
    Investments
    """

    return round(
        borrowings -
        investments,
        2
    )


# ============================================================
# Asset Turnover
# ============================================================

def asset_turnover(
        sales: float,
        total_assets: float
) -> Optional[float]:

    if total_assets == 0:
        return None

    return round(
        sales /
        total_assets,
        2
    )


# ============================================================
# ROCE Cross Check
# ============================================================

def check_roce_difference(
        calculated_roce: Optional[float],
        source_roce: Optional[float],
        company: str,
        year: int
) -> bool:

    if calculated_roce is None:
        return False

    if source_roce is None:
        return False

    difference = abs(
        calculated_roce -
        source_roce
    )

    if difference > 5:

        logger.warning(
            f"{company}-{year} "
            f"ROCE mismatch "
            f"Calc={calculated_roce} "
            f"Source={source_roce}"
        )

        return True

    return False


# ============================================================
# ROE Cross Check
# ============================================================

def check_roe_difference(
        calculated_roe: Optional[float],
        source_roe: Optional[float],
        company: str,
        year: int
) -> bool:

    if calculated_roe is None:
        return False

    if source_roe is None:
        return False

    difference = abs(
        calculated_roe -
        source_roe
    )

    if difference > 5:

        logger.warning(
            f"{company}-{year} "
            f"ROE mismatch "
            f"Calc={calculated_roe} "
            f"Source={source_roe}"
        )

        return True

    return False


# ============================================================
# Composite Quality Score
# ============================================================

def quality_score(
        roe: Optional[float],
        roce: Optional[float],
        npm: Optional[float],
        de: Optional[float]
) -> Optional[float]:

    score = 0

    if roe is not None and roe > 15:
        score += 25

    if roce is not None and roce > 15:
        score += 25

    if npm is not None and npm > 10:
        score += 25

    if de is not None and de < 1:
        score += 25

    return score


# ============================================================
# EBIT
# ============================================================

def ebit(
        operating_profit: float,
        other_income: float
) -> float:
    """
    Approximation

    EBIT =
    Operating Profit +
    Other Income
    """

    return operating_profit + other_income