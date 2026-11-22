def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places.

    For such prices the binary error in x*100 is < ~2e-8 cents, while
    a non-tie 4-dp price is at least 0.01 cent from the tie point.
    Adding 0.500001 (sign-aware, int() truncates toward zero) therefore
    recovers the exact decimal rounding, including ties like 2.675
    whose binary value is slightly below the tie.
    """
    try:
        return [
            int(x * 100.0 + (0.500001 if x >= 0.0 else -0.500001)) / 100.0
            for x in xs
        ]
    except Exception:
        # Fallback for non-float inputs (str, Decimal, ...): original logic.
        out = []
        for x in xs:
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
            out.append(-value if neg else value)
        return out
