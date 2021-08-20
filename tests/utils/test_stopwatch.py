""" Tests for superai.utils.stopwatch """

import logging

from superai.utils import stopwatch


@stopwatch
def fibonacci(n):
    """Fibonacci series

    0, 1, 1, 2, 3, 5, 8, 13, ...
    """
    if n <= 1:
        return n
    a = 0
    b = 1
    c = 1
    for i in range(2, n):
        a = b
        b = c
        c = a + b
    return c


def test_stopwatch(caplog):
    """Basic stopwatch test"""
    func = fibonacci
    with caplog.at_level(logging.DEBUG):
        func(100)

    assert f"{__name__}" in caplog.text, "Module name is logged using stopwatch"
    assert f"{fibonacci.__name__}()" in caplog.text, "Function name is logged using stopwatch"
    assert f"elapsed time: " in caplog.text, "Elapsed time logged using stopwatch"
