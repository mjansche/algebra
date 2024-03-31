def times_integer_power(a, b, exponent):
    """Returns a * b**exponent for non-negative integer exponents."""
    n = int(exponent)
    if n != exponent or n < 0:
        raise ValueError(f"cannot handle exponent {exponent}")
    while n > 0:
        if n & 1:
            a *= b
        b *= b
        n >>= 1
    return a


def group_integer_power(G, b, exponent):
    """Returns b**exponent for integer exponents."""
    n = int(exponent)
    if n != exponent:
        raise ValueError(f"cannot handle exponent {exponent}")
    n = abs(n)
    a = G.identity()
    while n > 0:
        if n & 1:
            a = G.op(a, b)
        b = G.op(b, b)
        n >>= 1
    if exponent < 0:
        a = G.inv(a)
    return a
