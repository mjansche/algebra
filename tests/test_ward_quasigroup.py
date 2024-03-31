import itertools

import pytest

from algebra import assertion
from algebra.ward_quasigroup import WardQuasigroup


def W1():
    return WardQuasigroup([1], lambda a, b: 1)


def W2():
    S = [0, 1]
    div = [
        [1, 0],
        [0, 1],
    ]
    return WardQuasigroup(S, lambda a, b: div[a][b])


def W3():
    S = [0, 1, 2]
    div = [
        [1, 0, 2],
        [2, 1, 0],
        [0, 2, 1],
    ]
    return WardQuasigroup(S, lambda a, b: div[a][b])


def V():
    S = [0, 1, 2, 3]
    div = [
        [0, 1, 2, 3],
        [1, 0, 3, 2],
        [2, 3, 0, 1],
        [3, 2, 1, 0],
    ]
    return WardQuasigroup(S, lambda a, b: div[a][b])


def D6():
    S = ["r0", "r1", "r2", "s0", "s1", "s2"]
    r0, r1, r2, s0, s1, s2 = S
    div = {
        (r0, r0): r0,
        (r0, r1): r2,
        (r0, r2): r1,
        (r0, s0): s0,
        (r0, s1): s1,
        (r0, s2): s2,
        (r1, r0): r1,
        (r1, r1): r0,
        (r1, r2): r2,
        (r1, s0): s2,
        (r1, s1): s0,
        (r1, s2): s1,
        (r2, r0): r2,
        (r2, r1): r1,
        (r2, r2): r0,
        (r2, s0): s1,
        (r2, s1): s2,
        (r2, s2): s0,
        (s0, r0): s0,
        (s0, r1): s2,
        (s0, r2): s1,
        (s0, s0): r0,
        (s0, s1): r1,
        (s0, s2): r2,
        (s1, r0): s1,
        (s1, r1): s0,
        (s1, r2): s2,
        (s1, s0): r2,
        (s1, s1): r0,
        (s1, s2): r1,
        (s2, r0): s2,
        (s2, r1): s1,
        (s2, r2): s0,
        (s2, s0): r1,
        (s2, s1): r2,
        (s2, s2): r0,
    }
    return WardQuasigroup(S, lambda x, y: div[x, y])


WARD_QUASIGROUPS = [W1(), W2(), W3(), V(), D6()]


# The tests here closely follow the structure of Ward's original paper:
#
# Morgan Ward (1930). "Postulates for the inverse operations in a group."
# Transactions of the American Mathematical Society, 32 (3): 520–526.


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_postulate_1(S):
    for a, b in itertools.product(S, repeat=2):
        assert a / b in S


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_postulate_2(S):
    for a, b in itertools.product(S, repeat=2):
        assert a / a == b / b


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_postulate_3(S):
    i = S.right_identity()
    for a, b, c in itertools.product(S, repeat=3):
        assert (a / b) / c == a / (c / (i / b))


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_postulate_4(S):
    i = S.right_identity()
    for a, b in itertools.product(S, repeat=2):
        assert (i / a == i / b) <= (a == b)


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_1(S):
    assert len({a for a in S if a / a == a}) == 1
    i = S.right_identity()
    assert i / i == i


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_2(S):
    i = S.right_identity()
    for a in S:
        assert i / a == (i / i) / a
        assert i / a == i / (a / (i / i))
        assert i / a == i / (a / i)
        assert a == a / i


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_3(S):
    i = S.right_identity()
    for a in S:
        assert i / a == (i / a) / i
        assert i / a == i / (i / (i / a))
        assert a == i / (i / a)


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_4(S):
    i = S.right_identity()
    for a, b, c in itertools.product(S, repeat=3):
        assert a / (b / c) == a / (b / (i / (i / c)))
        assert a / (b / c) == (a / (i / c)) / b


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_4_1(S):
    i = S.right_identity()
    for a, b in itertools.product(S, repeat=2):
        assert i / (a / b) == (i / (i / b)) / a
        assert i / (a / b) == b / a


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_5(S):
    i = S.right_identity()
    for a, b, c in itertools.product(S, repeat=3):
        assert (b / a == c / a) <= (b == c)
        assert (a / b == a / c) <= (b == c)
    for a, b in itertools.product(S, repeat=2):
        assert (i / a) / (b / a) == ((i / a) / (i / a)) / b
        assert (i / a) / (b / a) == i / b


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_cancellation(S):
    for a in S:
        assert {a / b for b in S} == set(S)
        assert {b / a for b in S} == set(S)


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_6(S):
    i = S.right_identity()
    for a, b, c in itertools.product(S, repeat=3):
        assert (a / b == c) <= (b == (i / c) / (i / a))
        assert (b == (i / c) / (i / a)) <= (a == c / (i / b))
        assert (a == c / (i / b)) <= (a / b == c)


# Definition 2: x ▱ y
def H(x, y):
    i = x / x
    return y / (i / x)


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_fundamental_theorem(S):
    i = S.right_identity()
    assertion.is_associative(H, S)
    assertion.is_identity(i, H, S)
    assertion.has_inverses(i, H, lambda x: i / x, S)


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_7(S):
    i = S.right_identity()
    for a, b, c in itertools.product(S, repeat=3):
        if H(b, c) == a:
            assert c == H(i / b, a)
            assert c == a / b
            assert b == H(a, i / c)
            assert b == (i / c) / (i / a)


# Definition 3: x ∆ y
def G(x, y):
    i = x / x
    return (i / x) / (i / y)


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_8(S):
    i = S.right_identity()
    for a in S:
        assert G(a, a) == i
        assert G(a, i) == i / a
        assert G(i, a) == a
        assert G(G(a, i), i) == a
    for a, b in itertools.product(S, repeat=2):
        assert G(G(a, b), i) == G(b, a)
        assert i / G(a, b) == G(b, a)


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_9(S):
    i = S.right_identity()
    for a, b, c in itertools.product(S, repeat=3):
        assert G(a, G(b, c)) == G(G(G(b, i), a), c)
        assert G(G(a, b), c) == G(b, G(G(a, i), c))


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_10(S):
    for a, b, c in itertools.product(S, repeat=3):
        assert (G(a, b) == G(a, c)) <= (b == c)
        assert (G(b, a) == G(c, a)) <= (b == c)


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_11(S):
    for a, b, c in itertools.product(S, repeat=3):
        assert (b == G(c, a)) <= (a / b == c)
        assert (b == G(c, a)) <= (H(b, c) == a)


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_12(S):
    for a, b in itertools.product(S, repeat=2):
        assert G(a, b) in S
        assert G(a, a) == G(b, b)
    i = S.right_identity()
    for a, b, c in itertools.product(S, repeat=3):
        assert G(G(a, b), c) == G(b, G(G(a, i), c))
    for a, b in itertools.product(S, repeat=2):
        assert (G(a, i) == G(b, i)) <= (a == b)


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_theorem_13(S):
    assert all(
        G(a, b) == b / a for a, b in itertools.product(S, repeat=2)
    ) == all(
        H(a, b) == H(b, a) for a, b in itertools.product(S, repeat=2)
    )


@pytest.mark.parametrize("S", WARD_QUASIGROUPS)
def test_inverses(S):
    for x, y in itertools.product(S, repeat=2):
        z = x / y
        assert y == G(z, x)
        assert x == H(y, z)
    for y, z in itertools.product(S, repeat=2):
        x = H(y, z)
        assert z == x / y
        assert y == G(z, x)
    for z, z in itertools.product(S, repeat=2):
        y = G(z, x)
        assert x == H(y, z)
        assert z == x / y
