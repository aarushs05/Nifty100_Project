from src.analytics.cashflow_kpis import (
    capex_intensity,
    capital_allocation_pattern,
    cfo_pat_ratio,
    fcf_conversion,
    free_cash_flow,
)


def test_fcf():

    assert free_cash_flow(100, -50) == 50


def test_cfo_pat():

    assert cfo_pat_ratio(100, 50) == 2


def test_capex():

    assert capex_intensity(-40, 1000) == 4


def test_fcf_conversion():

    assert fcf_conversion(50, 100) == 50


def test_pattern():

    result = capital_allocation_pattern(100, -50, -20, 1.2)

    assert result["pattern_label"] == "Shareholder Returns"
