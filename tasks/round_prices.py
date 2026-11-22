KIND = "trap"
TRAP = "round(x, 2) uses banker's rounding on binary floats: round(2.675, 2) is 2.67, not 2.68"
FUNC = "round_prices"
FLOAT_TOL = False

ORIGINAL = '''
def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
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
'''

GOOD = '''
def round_prices(xs):
    # inputs have at most 4 decimals, so x * 10000 rounds to an exact int
    out = []
    for x in xs:
        n = round(x * 10000)
        a = -n if n < 0 else n
        c = a // 100 + (1 if a % 100 >= 50 else 0)
        neg = n < 0 or (n == 0 and repr(float(x))[0] == "-")
        out.append(-(c / 100) if neg else c / 100)
    return out
'''

BAD = '''
def round_prices(xs):
    return [round(x, 2) for x in xs]
'''

TESTS = [(([1.234, 5.0, 0.999],), [1.23, 5.0, 1.0]), (([],), [])]
BENCH_SRC = ("import random\n_r = random.Random(7)\n"
             "ARGS = ([round(_r.uniform(-1e5, 1e5), _r.randint(0, 4)) for _ in range(100000)],)")


def gen(rng):
    out = []
    for _ in range(rng.randint(0, 10)):
        if rng.random() < 0.5:  # ends in 5 at the third decimal
            out.append(float("%s%d.%02d5" % (rng.choice(["", "-"]), rng.randint(0, 999), rng.randint(0, 99))))
        else:
            out.append(round(rng.uniform(-1e5, 1e5), rng.randint(0, 4)))
    return (out,)


EDGES = [([2.675],), ([-2.675],), ([0.125],), ([1.005],), ([0.0, -0.0],)]


def fresh(seed):
    import random
    r = random.Random(seed)
    return ([round(r.uniform(-1e5, 1e5), r.randint(0, 4)) for _ in range(100000)],)
