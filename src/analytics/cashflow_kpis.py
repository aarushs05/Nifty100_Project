"""
Cash Flow KPI Engine
Sprint 2
"""

from __future__ import annotations

from typing import Optional


# ==========================================================
# Free Cash Flow
# ==========================================================

def free_cash_flow(
        operating_activity: float,
        investing_activity: float
) -> float:
    """
    FCF

    CFO + Investing Activity

    Investing Activity is generally
    negative, therefore addition
    naturally subtracts CapEx.
    """

    return round(
        operating_activity +
        investing_activity,
        2
    )


# ==========================================================
# CFO Quality
# ==========================================================

def cfo_pat_ratio(
        operating_activity: float,
        net_profit: float
) -> Optional[float]:

    if net_profit == 0:
        return None

    return round(
        operating_activity /
        net_profit,
        2
    )


def average_cfo_quality(
        ratios
) -> Optional[float]:

    valid = [
        x for x in ratios
        if x is not None
    ]

    if len(valid) == 0:
        return None

    return round(
        sum(valid) /
        len(valid),
        2
    )


def cfo_quality_label(
        average_ratio: Optional[float]
) -> Optional[str]:

    if average_ratio is None:
        return None

    if average_ratio > 1:
        return "High Quality"

    if average_ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


# ==========================================================
# CapEx Intensity
# ==========================================================

def capex_intensity(
        investing_activity: float,
        sales: float
) -> Optional[float]:

    if sales == 0:
        return None

    value = (
        abs(investing_activity) /
        sales
    ) * 100

    return round(
        value,
        2
    )


def capex_label(
        intensity: Optional[float]
) -> Optional[str]:

    if intensity is None:
        return None

    if intensity < 3:
        return "Asset Light"

    if intensity <= 8:
        return "Moderate"

    return "Capital Intensive"


# ==========================================================
# FCF Conversion
# ==========================================================

def fcf_conversion(
        free_cash_flow_value: float,
        operating_profit: float
) -> Optional[float]:

    if operating_profit == 0:
        return None

    return round(
        (
            free_cash_flow_value /
            operating_profit
        ) * 100,
        2
    )

# ==========================================================
# Capital Allocation Pattern
# ==========================================================

def sign(value: float) -> str:
    """
    Return '+' or '-' depending on value.
    Zero is treated as positive.
    """
    if value >= 0:
        return "+"
    return "-"


def capital_allocation_pattern(
        operating_activity: float,
        investing_activity: float,
        financing_activity: float,
        cfo_quality: Optional[float] = None
):
    """
    8-pattern capital allocation classifier
    """

    cfo = sign(operating_activity)
    cfi = sign(investing_activity)
    cff = sign(financing_activity)

    pattern = (cfo, cfi, cff)

    # (+,-,-)
    if pattern == ("+", "-", "-"):

        if (
            cfo_quality is not None and
            cfo_quality > 1
        ):
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"

    # (+,+,-)
    elif pattern == ("+", "+", "-"):
        label = "Liquidating Assets"

    # (-,+,+)
    elif pattern == ("-", "+", "+"):
        label = "Distress Signal"

    # (-,-,+)
    elif pattern == ("-", "-", "+"):
        label = "Growth Funded by Debt"

    # (+,+,+)
    elif pattern == ("+", "+", "+"):
        label = "Cash Accumulator"

    # (-,-,-)
    elif pattern == ("-", "-", "-"):
        label = "Pre-Revenue"

    # (+,-,+)
    elif pattern == ("+", "-", "+"):
        label = "Mixed"

    # (-,+,-)
    elif pattern == ("-", "+", "-"):
        label = "Restructuring"

    else:
        label = "Unknown"

    return {
        "cfo_sign": cfo,
        "cfi_sign": cfi,
        "cff_sign": cff,
        "pattern_label": label
    }


# ==========================================================
# Batch Cashflow KPIs
# ==========================================================

def compute_cashflow_metrics(
        operating_activity,
        investing_activity,
        financing_activity,
        sales,
        operating_profit,
        net_profit,
        quality_history=None
):

    if quality_history is None:
        quality_history = []

    fcf = free_cash_flow(
        operating_activity,
        investing_activity
    )

    ratio = cfo_pat_ratio(
        operating_activity,
        net_profit
    )

    quality_history.append(ratio)

    avg_quality = average_cfo_quality(
        quality_history
    )

    capex = capex_intensity(
        investing_activity,
        sales
    )

    allocation = capital_allocation_pattern(
        operating_activity,
        investing_activity,
        financing_activity,
        avg_quality
    )

    return {

        "free_cash_flow": fcf,

        "fcf_conversion":
            fcf_conversion(
                fcf,
                operating_profit
            ),

        "capex_intensity": capex,

        "capex_label":
            capex_label(capex),

        "cfo_pat_ratio": ratio,

        "cfo_quality_score":
            avg_quality,

        "cfo_quality_label":
            cfo_quality_label(avg_quality),

        **allocation
    }


# ==========================================================
# CSV Record Builder
# ==========================================================

def build_capital_allocation_record(
        company_id,
        year,
        allocation
):

    return {
        "company_id": company_id,
        "year": year,
        "cfo_sign": allocation["cfo_sign"],
        "cfi_sign": allocation["cfi_sign"],
        "cff_sign": allocation["cff_sign"],
        "pattern_label": allocation["pattern_label"]
    }


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    result = compute_cashflow_metrics(

        operating_activity=120,

        investing_activity=-45,

        financing_activity=-30,

        sales=650,

        operating_profit=160,

        net_profit=110,

        quality_history=[1.2, 1.1, 0.95, 1.08]

    )

    for key, value in result.items():
        print(f"{key} : {value}")