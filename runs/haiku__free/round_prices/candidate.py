def _round_one(x):
    """Slow path, identical to the original per-price logic. Used for
    reprs that are not plain decimal (scientific notation, inf, nan)."""
    s = repr(float(x))
    neg = False
    whole = 0
    frac = []
    seen_dot = False
    for ch in s:
        if ch == "-":
            neg = True
        elif ch == ".":
            seen_dot = True
        elif seen_dot:
            frac.append(int(ch))
        else:
            whole = whole * 10 + int(ch)
    while len(frac) < 3:
        frac.append(0)
    cents = whole * 100 + frac[0] * 10 + frac[1]
    if frac[2] >= 5:
        cents += 1
    value = cents / 100
    return -value if neg else value


def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    out = []
    append = out.append
    for x in xs:
        s = repr(float(x))
        if "e" in s or "." not in s:
            append(_round_one(x))
            continue
        neg = s[0] == "-"
        if neg:
            s = s[1:]
        ip, _, fp = s.partition(".")
        p = fp + "000"
        # ip + first two decimals form the cents as one integer string
        cents = int(ip + p[:2])
        if p[2] >= "5":
            cents += 1
        value = cents / 100
        append(-value if neg else value)
    return out
