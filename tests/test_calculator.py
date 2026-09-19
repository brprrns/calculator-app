import pytest
from calculator import add, subtract, multiply


@pytest.mark.parametrize("a,b,expected", [(1, 1, 2), (2, 3, 5), (10**12, 1, 10**12 + 1)])
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [(10, 3, 7), (5, 5, 0), (3, 10, -7)])
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [(4, 5, 20), (1, 9, 9)])
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize("fn", [add, subtract, multiply])
@pytest.mark.parametrize("a,b", [(0, 1), (-1, 2), (1, -2)])
def test_non_positive_rejected(fn, a, b):
    with pytest.raises(ValueError):
        fn(a, b)


@pytest.mark.parametrize("fn", [add, subtract, multiply])
@pytest.mark.parametrize("a,b", [(1.5, 2), ("3", 4), (True, 2), (None, 1)])
def test_wrong_type_rejected(fn, a, b):
    with pytest.raises(TypeError):
        fn(a, b)