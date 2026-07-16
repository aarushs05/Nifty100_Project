from src.analytics.cagr import (

    calculate_cagr,

    TURNAROUND,

    DECLINE_TO_LOSS,

    BOTH_NEGATIVE,

    ZERO_BASE

)


def test_normal_cagr():

    result=calculate_cagr(

        100,

        200,

        5

    )

    assert result.flag is None


def test_turnaround():

    result=calculate_cagr(

        -100,

        200,

        5

    )

    assert result.flag==TURNAROUND


def test_decline():

    result=calculate_cagr(

        100,

        -100,

        5

    )

    assert result.flag==DECLINE_TO_LOSS


def test_both_negative():

    result=calculate_cagr(

        -100,

        -200,

        5

    )

    assert result.flag==BOTH_NEGATIVE


def test_zero_base():

    result=calculate_cagr(

        0,

        100,

        5

    )

    assert result.flag==ZERO_BASE