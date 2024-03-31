from .format import superscript
from .power import times_integer_power


class FreeGroup:

    def __init__(self, generators):
        self._generators = tuple(generators)
        assert self._generators

    def __repr__(self):
        d = ", ".join(str(g) for g in self._generators)
        return f"FreeGroup({d})"

    def order(self):
        return float("inf")

    def rank(self):
        return len(self._generators)

    def generators(self):
        for g in self._generators:
            yield FreeGroupElement([(g, 1)])

    def identity(self):
        return FreeGroupElement([])

    def one(self):
        return self.identity()

    def inv(self, a):
        assert isinstance(a, FreeGroupElement)
        return a.inv()

    def op(self, a, b):
        assert isinstance(a, FreeGroupElement)
        assert isinstance(b, FreeGroupElement)
        return a * b

    def rep(self, a, n):
        assert isinstance(a, FreeGroupElement)
        return a**n


class FreeGroupElement:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        if not self.value:
            return "1"
        return " ".join(f"{g}" if e == 1 else f"{g}{superscript(e)}" for g, e in self.value)

    def __eq__(self, other):
        return self is other or self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(tuple(self.value))

    def inv(self):
        return FreeGroupElement([(g, -e) for g, e in reversed(self.value)])

    def __mul__(self, other):
        a = self.value
        if not a:
            return other
        b = other.value
        if not b:
            return self
        i = len(a)
        j = 0
        while i > 0 and j < len(b):
            x, m = a[i - 1]
            y, n = b[j]
            if x != y:
                break
            k = m + n
            if k != 0:
                return FreeGroupElement(a[: i - 1] + [(x, k)] + b[j + 1 :])
            i -= 1
            j += 1
        return FreeGroupElement(a[:i] + b[j:])

    def __pow__(self, exponent, mod=None):
        n = int(exponent)
        if n == exponent:
            one = FreeGroupElement([])
            result = times_integer_power(one, self, abs(n))
            if n < 0:
                result = result.inv()
            return result
        raise ValueError(f"cannot handle exponent {exponent}")
