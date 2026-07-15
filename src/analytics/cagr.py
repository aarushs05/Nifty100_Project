"""
CAGR Engine
Sprint 2

Computes CAGR for Revenue, PAT and EPS
with complete edge-case handling.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import math


# ======================================================
# CAGR Result Object
# ======================================================

@dataclass
class CAGRResult:

    value: Optional[float]

    flag: Optional[str]


# ======================================================
# Flags
# ======================================================

TURNAROUND = "TURNAROUND"

DECLINE_TO_LOSS = "DECLINE_TO_LOSS"

BOTH_NEGATIVE = "BOTH_NEGATIVE"

ZERO_BASE = "ZERO_BASE"

INSUFFICIENT = "INSUFFICIENT"

NORMAL = None


# ======================================================
# Helper
# ======================================================

def has_enough_data(values, years_required):

    if values is None:
        return False

    return len(values) >= years_required + 1


# ======================================================
# Generic CAGR
# ======================================================

def calculate_cagr(
        start_value: float,
        end_value: float,
        years: int
) -> CAGRResult:

    # zero base

    if start_value == 0:

        return CAGRResult(
            None,
            ZERO_BASE
        )

    # insufficient years

    if years <= 0:

        return CAGRResult(
            None,
            INSUFFICIENT
        )

    # turnaround

    if start_value < 0 and end_value > 0:

        return CAGRResult(
            None,
            TURNAROUND
        )

    # decline to loss

    if start_value > 0 and end_value < 0:

        return CAGRResult(
            None,
            DECLINE_TO_LOSS
        )

    # both negative

    if start_value < 0 and end_value < 0:

        return CAGRResult(
            None,
            BOTH_NEGATIVE
        )

    value = (
        (
            end_value /
            start_value
        ) ** (
            1 / years
        ) - 1
    ) * 100

    return CAGRResult(
        round(value, 2),
        NORMAL
    )


# ======================================================
# Revenue CAGR
# ======================================================

def revenue_cagr(
        sales_history,
        years
):

    if not has_enough_data(
            sales_history,
            years):

        return CAGRResult(
            None,
            INSUFFICIENT
        )

    start = sales_history[-(years + 1)]

    end = sales_history[-1]

    return calculate_cagr(
        start,
        end,
        years
    )


# ======================================================
# PAT CAGR
# ======================================================

def pat_cagr(
        profit_history,
        years
):

    if not has_enough_data(
            profit_history,
            years):

        return CAGRResult(
            None,
            INSUFFICIENT
        )

    start = profit_history[-(years + 1)]

    end = profit_history[-1]

    return calculate_cagr(
        start,
        end,
        years
    )



# ======================================================
# EPS CAGR
# ======================================================

def eps_cagr(
        eps_history,
        years
):

    if not has_enough_data(
            eps_history,
            years):

        return CAGRResult(
            None,
            INSUFFICIENT
        )

    start = eps_history[-(years + 1)]

    end = eps_history[-1]

    return calculate_cagr(
        start,
        end,
        years
    )


# ======================================================
# Window Wrappers
# ======================================================

def revenue_cagr_3yr(history):
    return revenue_cagr(history, 3)


def revenue_cagr_5yr(history):
    return revenue_cagr(history, 5)


def revenue_cagr_10yr(history):
    return revenue_cagr(history, 10)


def pat_cagr_3yr(history):
    return pat_cagr(history, 3)


def pat_cagr_5yr(history):
    return pat_cagr(history, 5)


def pat_cagr_10yr(history):
    return pat_cagr(history, 10)


def eps_cagr_3yr(history):
    return eps_cagr(history, 3)


def eps_cagr_5yr(history):
    return eps_cagr(history, 5)


def eps_cagr_10yr(history):
    return eps_cagr(history, 10)


# ======================================================
# Batch Calculation
# ======================================================

def compute_all_cagr(
        revenue_history,
        pat_history,
        eps_history
):

    return {

        "revenue_cagr_3yr":
            revenue_cagr_3yr(revenue_history),

        "revenue_cagr_5yr":
            revenue_cagr_5yr(revenue_history),

        "revenue_cagr_10yr":
            revenue_cagr_10yr(revenue_history),

        "pat_cagr_3yr":
            pat_cagr_3yr(pat_history),

        "pat_cagr_5yr":
            pat_cagr_5yr(pat_history),

        "pat_cagr_10yr":
            pat_cagr_10yr(pat_history),

        "eps_cagr_3yr":
            eps_cagr_3yr(eps_history),

        "eps_cagr_5yr":
            eps_cagr_5yr(eps_history),

        "eps_cagr_10yr":
            eps_cagr_10yr(eps_history),
    }


# ======================================================
# SQLite Record
# ======================================================

def cagr_to_record(results):

    record = {}

    for key, value in results.items():

        record[key] = value.value

        record[f"{key}_flag"] = value.flag

    return record


# ======================================================
# Utility
# ======================================================

def print_cagr(result: CAGRResult):

    if result.value is None:

        print(
            f"CAGR : None | Flag : {result.flag}"
        )

    else:

        print(
            f"CAGR : {result.value:.2f}%"
        )


# ======================================================
# Example
# ======================================================

if __name__ == "__main__":

    revenue = [
        100,
        120,
        145,
        180,
        210,
        260
    ]

    pat = [
        12,
        16,
        18,
        24,
        29,
        38
    ]

    eps = [
        5,
        5.6,
        6.1,
        7.8,
        8.4,
        10.5
    ]

    results = compute_all_cagr(
        revenue,
        pat,
        eps
    )

    for name, value in results.items():

        print(
            name,
            value
        )