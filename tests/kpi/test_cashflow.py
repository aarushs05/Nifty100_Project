from src.analytics.cashflow_kpis import (

    free_cash_flow,

    cfo_pat_ratio,

    capex_intensity,

    fcf_conversion,

    capital_allocation_pattern

)


def test_fcf():

    assert free_cash_flow(

        100,

        -50

    )==50


def test_cfo_pat():

    assert cfo_pat_ratio(

        100,

        50

    )==2


def test_capex():

    assert capex_intensity(

        -40,

        1000

    )==4


def test_fcf_conversion():

    assert fcf_conversion(

        50,

        100

    )==50


def test_pattern():

    result=capital_allocation_pattern(

        100,

        -50,

        -20,

        1.2

    )

    assert result["pattern_label"]=="Shareholder Returns"