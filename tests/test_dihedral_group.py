import pytest

from algebra import assertion
from algebra.dihedral_group import D

DIHEDRAL_GROUPS = [D(n) for n in range(1, 21)]


@pytest.mark.parametrize("G", DIHEDRAL_GROUPS)
def test_associativity(G):
    assertion.is_associative(G.op, G)


@pytest.mark.parametrize("G", DIHEDRAL_GROUPS)
def test_identity(G):
    assertion.is_identity(G.identity(), G.op, G)
    e = G.one()
    for a in G:
        assert e * a == a
        assert a * e == a


@pytest.mark.parametrize("G", DIHEDRAL_GROUPS)
def test_inverse(G):
    e = G.one()
    for a in G:
        b = a.inv()
        assert a * b == e
        assert b * a == e


@pytest.mark.parametrize("G", DIHEDRAL_GROUPS[:2])
def test_commutative(G):
    assertion.is_commutative(G.op, G)


@pytest.mark.parametrize("G", DIHEDRAL_GROUPS)
def test_power(G):
    e = G.one()
    for a in G:
        ak = e
        for k in range(G.order()):
            assert ak == a**k
            assert ak * a**-k == e
            assert a**-k * ak == e
            ak = ak * a


@pytest.mark.parametrize("G", [D(n) for n in (5, 7, 11, 13, 17)])
def test_root(G):
    for k in range(3, G.degree(), 2):
        for a in G:
            assert (a ** (1 / k)) ** k == a
            assert (a**k) ** (1 / k) == a
