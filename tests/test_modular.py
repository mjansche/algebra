import itertools
import math

import pytest

from algebra import modular


@pytest.mark.parametrize("a,b", itertools.product(range(-10, 10), repeat=2))
def test_bezout(a, b):
    x, y, gcd = modular.bezout(a, b)
    assert a * x + b * y == gcd
    assert abs(gcd) == math.gcd(a, b)
    assert (gcd == 0) == (a == 0 and b == 0)
    if a != 0 and b != 0:
        assert gcd != 0
        assert abs(x) < b // gcd
        assert abs(y) <= abs(a // gcd)


@pytest.mark.parametrize("m,n", itertools.product(range(1, 11), repeat=2))
def test_crt(m, n):
    gcd = math.gcd(m, n)
    for a in range(m):
        for b in range(n):
            if (a % gcd) != (b % gcd):
                continue
            c, lcm = modular.crt(a, m, b, n)
            assert lcm == m * n // gcd
            assert 0 <= c < lcm
            assert (c % m) == (a % m)
            assert (c % n) == (b % n)
