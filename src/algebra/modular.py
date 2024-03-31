def bezout(a, b):
    """Find (x, y, g) such that ax + by = g = gcd(a, b)."""
    if b == 0:
        return 1, 0, a
    prev_x, x = 1, 0
    prev_y, y = 0, 1
    while True:
        quotient, remainder = divmod(a, b)
        if remainder == 0:
            break
        a, b = b, remainder
        prev_x, x = x, prev_x - quotient * x
        prev_y, y = y, prev_y - quotient * y
    return x, y, b


def crt(a, m, b, n):
    """Find (c, lcm(m, n)) such that c ≡ a (mod m) and c ≡ b (mod n)."""
    assert m >= 1
    assert n >= 1
    x, y, gcd = bezout(m, n)
    if gcd < 0:
        x, y, gcd = -x, -y, -gcd
    if (a % gcd) != (b % gcd):
        raise ValueError(f"No solution, because {a} ≢ {b} (mod {gcd})")
    c = (a * y * n + b * x * m) // gcd
    lcm = m * n // gcd
    return c % lcm, lcm
