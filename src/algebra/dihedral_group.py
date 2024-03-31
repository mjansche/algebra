from .format import subscript
from .modular import crt
from .overload import Multiplicative
from .power import group_integer_power


def D(degree=None, *, order=None):
    assert degree is not None or order is not None
    if degree is None:
        assert order % 2 == 0
        degree = order // 2
    assert degree > 0
    if order is not None:
        assert order == 2 * degree
    return Multiplicative(DihedralGroup(degree))


class DihedralGroup:

    def __init__(self, n):
        self._n = n

    def __repr__(self):
        return f"D{subscript(self._n)}"

    def degree(self):
        return self._n

    def order(self):
        return 2 * self._n

    def pretty(self, a):
        rot, i = a
        return f"{'r' if rot else 's'}{subscript(i)}"

    def __iter__(self):
        for i in range(self._n):
            yield True, i
        for i in range(self._n):
            yield False, i

    def identity(self):
        return True, 0

    def inv(self, a):
        rot, i = a
        if rot:
            return True, -i % self._n
        return a

    def op(self, a, b):
        rot1, i = a
        rot2, j = b
        if not rot1:
            j = -j
        return rot1 == rot2, (i + j) % self._n

    def rep(self, a, exponent):
        n = int(exponent)
        if n == exponent:
            return group_integer_power(self, a, n)
        r = 1 / exponent
        n = round(r)
        if 0 < n < 2**52 and abs((n - r) / n) < 2e-16:
            return self._root(a, n)
        raise ValueError(f"cannot handle exponent {exponent}")

    def _root(self, a, n):
        k = int(n)
        assert k == n
        rot, i = a
        if rot:
            j, _ = crt(i, self._n, 0, k)
            j //= k
            assert 0 <= j < self._n
            return True, j
        else:
            if k % 2 == 1:
                return a
            else:
                raise ValueError(f"{self.pretty(a)} has no even roots")
