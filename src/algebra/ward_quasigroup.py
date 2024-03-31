"""
Morgan Ward (1930). "Postulates for the inverse operations in a group."
Transactions of the American Mathematical Society, 32 (3): 520–526.
"""


class WardQuasigroup:

    def __init__(self, S, div):
        self.S = S
        self._div = div

    def __len__(self):
        return len(self.S)

    def __iter__(self):
        for a in self.S:
            yield WardQuasigroupElement(self._div, a)

    def __contains__(self, element):
        return isinstance(element, WardQuasigroupElement) and element.value in self.S

    def right_identity(self):
        a = next(iter(self))
        return a / a


class WardQuasigroupElement:

    def __init__(self, div, value):
        self.div = div
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    def _wrap(self, value):
        return WardQuasigroupElement(self.div, value)

    def __truediv__(self, other):
        return self._wrap(self.div(self.value, other.value))

    def __mul__(self, other):
        i = self / self
        return other / (i / self)

    def __xor__(self, other):
        i = self / self
        return (i / self) / (i / other)
