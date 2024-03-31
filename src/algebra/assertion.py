import itertools


def is_associative(f, elements):
    for a, b, c in itertools.product(elements, repeat=3):
        assert f(f(a, b), c) == f(a, f(b, c)), (
            f"f(f({a}, {b}), {c}) == {f(f(a, b), c)} != {f(a, f(b, c))} == f({a}, f({b}, {c}))"
        )


def is_commutative(f, elements):
    for a, b in itertools.product(elements, repeat=2):
        assert f(a, b) == f(b, a), f"f({a}, {b}) == {f(a, b)} != {f(b, a)} = f({b}, {a})"


def is_left_identity(e, f, elements):
    for a in elements:
        assert f(e, a) == a, f"f({e}, {a}) == {f(e, a)} != {a}"


def is_right_identity(e, f, elements):
    for a in elements:
        assert f(a, e) == a, f"f({a}, {e}) == {f(a, e)} != {a}"


def is_identity(e, f, elements):
    is_left_identity(e, f, elements)
    is_right_identity(e, f, elements)


def has_inverses(e, f, inv, elements):
    for a in elements:
        assert f(a, inv(a)) == e
        assert f(inv(a), a) == e


def left_distributes_over(f, g, elements):
    for a, b, c in itertools.product(elements, repeat=3):
        assert f(a, g(b, c)) == g(f(a, b), f(a, c))


def right_distributes_over(f, g, elements):
    for a, b, c in itertools.product(elements, repeat=3):
        assert f(g(a, b), c) == g(f(a, c), f(b, c))


def distributes_over(f, g, elements):
    left_distributes_over(f, g, elements)
    right_distributes_over(f, g, elements)
