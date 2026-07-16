import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets
)


def test_net_profit_margin():

    assert net_profit_margin(100,1000)==10


def test_net_profit_margin_zero_sales():

    assert net_profit_margin(100,0) is None


def test_operating_margin():

    assert operating_profit_margin(250,1000)==25


def test_roe():

    assert return_on_equity(
        100,
        200,
        300
    )==20


def test_roe_negative_equity():

    assert return_on_equity(
        100,
        -200,
        100
    ) is None


def test_roce():

    assert round(

        return_on_capital_employed(

            200,

            100,

            400,

            500

        ),

        2

    )==20


def test_roa():

    assert return_on_assets(

        200,

        1000

    )==20