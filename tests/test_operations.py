import pytest

from calculator.operations import add, subtract, multiply


def test_add():
    assert add(10, 5) == 15


def test_subtract():
    assert subtract(10, 5) == 5


def test_subtract_can_go_negative():
    # inputs must be positive, the result doesn't have to be
    assert subtract(2, 5) == -3


def test_multiply():
    assert multiply(10, 5) == 50


@pytest.mark.parametrize("func", [add, subtract, multiply])
@pytest.mark.parametrize("bad", [0, -1, -100])
def test_rejects_zero_and_negative(func, bad):
    with pytest.raises(ValueError):
        func(bad, 5)
    with pytest.raises(ValueError):
        func(5, bad)


@pytest.mark.parametrize("func", [add, subtract, multiply])
@pytest.mark.parametrize("bad", [2.5, "7", None, True])
def test_rejects_non_integers(func, bad):
    with pytest.raises(ValueError):
        func(bad, 5)
