from src.analytics.ratios import (

    debt_to_equity,

    interest_coverage_ratio,

    asset_turnover,

    net_debt,

    high_leverage_flag,

    icr_warning_flag

)


def test_debt_free():

    assert debt_to_equity(

        0,

        100,

        200

    )==0


def test_debt_equity():

    assert debt_to_equity(

        300,

        100,

        200

    )==1


def test_interest_coverage():

    assert interest_coverage_ratio(

        500,

        100,

        100

    )==6


def test_interest_none():

    assert interest_coverage_ratio(

        100,

        100,

        0

    ) is None


def test_asset_turnover():

    assert asset_turnover(

        1000,

        500

    )==2


def test_net_debt():

    assert net_debt(

        1000,

        300

    )==700


def test_high_leverage():

    assert high_leverage_flag(

        6,

        "Technology"

    )==True


def test_interest_warning():

    assert icr_warning_flag(

        1

    )==True