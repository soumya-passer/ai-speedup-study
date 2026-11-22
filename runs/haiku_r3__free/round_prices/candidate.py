def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    out = []
    append = out.append
    for x in xs:
        s = repr(float(x))
        if "e" in s or "n" in s:
            # Exponent form or inf/nan: keep the original digit-by-digit path.
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
            append(-value if neg else value)
            continue
        neg = s[0] == "-"
        if neg:
            s = s[1:]
        whole, _, fracpart = s.partition(".")
        f = (fracpart + "000")[:3]
        cents = int(whole) * 100 + int(f[:2])
        if f[2] >= "5":
            cents += 1
        value = cents / 100
        append(-value if neg else value)
    return out
