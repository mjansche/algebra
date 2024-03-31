"""Wrappers that provide overloaded operators for elements of structures."""

import abc

from .power import group_integer_power


class GroupWrapper:
    """Group wrapper base class."""

    def __init__(self, G):
        self.G = G

    def __getattr__(self, attr):
        return getattr(self.G, attr)

    def __repr__(self):
        return f"{self.NAME}({self.G!r})"

    def __str__(self):
        return f"{self.NAME}({self.G})"

    @abc.abstractmethod
    def _wrap(self, value):
        pass

    def __iter__(self):
        for a in self.G:
            yield self._wrap(a)

    def generators(self, *args, **kwargs):
        for a in self.G.generators(*args, **kwargs):
            yield self._wrap(a)

    def identity(self):
        return self._wrap(self.G.identity())

    def inv(self, a):
        assert isinstance(a, MultiplicativeGroupElement)
        return a.inv()

    def op(self, a, b):
        assert isinstance(a, MultiplicativeGroupElement)
        assert isinstance(b, MultiplicativeGroupElement)
        return a.op(b)

    def rep(self, a, multiplicity):
        assert isinstance(a, MultiplicativeGroupElement)
        return a.rep(multiplicity)


class Multiplicative(GroupWrapper):
    """Group wrapper that adds multiplicative overloads to elements."""

    NAME = "Multiplicative"

    def _wrap(self, value):
        return MultiplicativeGroupElement(self.G, value)

    def one(self):
        return self.identity()


class Additive(GroupWrapper):
    """Group wrapper that adds additive overloads to elements."""

    NAME = "Additive"

    def _wrap(self, value):
        return AdditiveGroupElement(self.G, value)

    def zero(self):
        return self.identity()


class GroupElement:

    def __init__(self, G, value):
        self.G = G
        self.value = value

    def __eq__(self, other):
        return self is other or (self.G == other.G and self.value == other.value)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.G) ^ hash(self.value)

    def __repr__(self):
        if hasattr(self.G, "pretty"):
            return self.G.pretty(self.value)
        return repr(self.value)

    @abc.abstractmethod
    def _wrap(self, value):
        pass

    def inv(self):
        return self._wrap(self.G.inv(self.value))

    def op(self, other):
        assert type(self) is type(other)
        assert self.G == other.G
        return self._wrap(self.G.op(self.value, other.value))

    def rep(self, multiplicity):
        if hasattr(self.G, "rep"):
            value = self.G.rep(self.value, multiplicity)
        else:
            value = group_integer_power(self.G, self.value, multiplicity)
        return self._wrap(value)


class MultiplicativeGroupElement(GroupElement):

    def _wrap(self, value):
        return MultiplicativeGroupElement(self.G, value)

    def __mul__(self, other):
        return self.op(other)

    def __pow__(self, exponent, mod=None):
        assert mod is None
        return self.rep(exponent)

    def __truediv__(self, other):
        return self * other.inv()

    def __xor__(self, other):
        r"""Abusing (x ^ y) to mean (x \ y) or (x^-1 * y)."""
        return self.inv() * other


class AdditiveGroupElement(GroupElement):

    def _wrap(self, value):
        return AdditiveGroupElement(self.G, value)

    def __add__(self, other):
        return self.op(other)

    def __pos__(self):
        return self

    def __neg__(self):
        return self.inv()

    def __sub__(self, other):
        return self + (-other)

    def __matmul__(self, multiplicity):
        """Abusing (x @ n) to mean (x + ... + x) with n terms."""
        return self.rep(multiplicity)
