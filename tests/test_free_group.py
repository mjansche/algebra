from functools import reduce
from itertools import permutations

import pytest

from algebra import assertion
from algebra.free_group import FreeGroup


FREE_GROUPS = [
    FreeGroup(["a"]),
    FreeGroup(["a", "b"]),
    FreeGroup(["a", "b", "c"]),
]


def gen_elements(G):
    elems = list(G.generators())
    for a in G.generators():
        elems.append(a.inv())
    for n in range(3):
        for p in permutations(elems, n):
            yield reduce(G.op, p, G.identity())


@pytest.mark.parametrize("G", FREE_GROUPS)
def test_associativity(G):
    assertion.is_associative(G.op, gen_elements(G))


@pytest.mark.parametrize("G", FREE_GROUPS)
def test_identity(G):
    assertion.is_identity(G.identity(), G.op, gen_elements(G))
    e = G.identity()
    for a in gen_elements(G):
        assert e * a == a
        assert a * e == a


@pytest.mark.parametrize("G", FREE_GROUPS)
def test_inverse(G):
    e = G.identity()
    for a in gen_elements(G):
        b = a.inv()
        assert a * b == e
        assert b * a == e


@pytest.mark.parametrize("G", [FreeGroup(["a"]), FreeGroup(["b"])])
def test_commutative(G):
    assertion.is_commutative(G.op, gen_elements(G))


@pytest.mark.parametrize("G", FREE_GROUPS)
def test_power(G):
    e = G.one()
    for a in gen_elements(G):
        ak = e
        for k in range(10):
            assert ak == a**k
            assert ak * a**-k == e
            assert a**-k * ak == e
            ak = ak * a
