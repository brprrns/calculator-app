def _check(value, name):
    # bool is a subclass of int in Python, so reject it explicitly
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def add(a, b):
    _check(a, "a"); _check(b, "b")
    return a + b


def subtract(a, b):
    _check(a, "a"); _check(b, "b")
    return a - b          # result may be 0 or negative; that is allowed


def multiply(a, b):
    _check(a, "a"); _check(b, "b")
    return a * b