"""Basic calculator operations.

The assignment says the calculator works on two *positive integers*,
so every function checks its inputs before doing any maths.
Note: subtract(2, 5) is allowed and gives -3. The inputs have to be
positive, the answer doesn't.
"""


def _check_positive_int(name, value):
    # bool is a subclass of int in Python (True == 1), so reject it explicitly
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be a positive integer, got {value!r}")
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer, got {value!r}")


def add(a, b):
    _check_positive_int("a", a)
    _check_positive_int("b", b)
    return a + b


def subtract(a, b):
    _check_positive_int("a", a)
    _check_positive_int("b", b)
    return a - b


def multiply(a, b):
    _check_positive_int("a", a)
    _check_positive_int("b", b)
    return a * b
