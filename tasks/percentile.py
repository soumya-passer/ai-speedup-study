KIND = "trap"
TRAP = "picking the nearest item instead of blending the two closest items, or using statistics.quantiles' different method"
FUNC = "percentile"
FLOAT_TOL = True

ORIGINAL = '''
def percentile(xs, p):
    """The p-th percentile (0 <= p <= 100) of a list of numbers, by linear
    blending: sort the list, find position r = p / 100 * (n - 1), and blend
    the items at floor(r) and floor(r) + 1 by the fraction part of r.
    Floats may differ from this function only by rounding (relative 1e-6).
    Raises ValueError on an empty list or p outside 0 to 100."""
    if not xs or p < 0 or p > 100:
        raise ValueError("bad input")
    s = []
    for x in xs:
        i = len(s)
        while i > 0 and s[i - 1] > x:
            i -= 1
        s.insert(i, x)
    r = p / 100 * (len(s) - 1)
    lo = int(r)
    frac = r - lo
    if lo + 1 < len(s):
        return s[lo] + (s[lo + 1] - s[lo]) * frac
    return float(s[lo]) if frac == 0 else s[lo] + 0.0
'''

GOOD = '''
def percentile(xs, p):
    if not xs or p < 0 or p > 100:
        raise ValueError("bad input")
    s = sorted(xs)
    r = p / 100 * (len(s) - 1)
    lo = int(r)
    frac = r - lo
    if lo + 1 < len(s):
        return s[lo] + (s[lo + 1] - s[lo]) * frac
    return float(s[lo]) if frac == 0 else s[lo] + 0.0
'''

BAD = '''
def percentile(xs, p):
    if not xs or p < 0 or p > 100:
        raise ValueError("bad input")
    s = sorted(xs)
    return s[round(p / 100 * (len(s) - 1))]
'''

TESTS = [(([1, 2, 3, 4, 5], 50), 3), (([10, 20, 30], 100), 30), (([7], 0), 7)]
BENCH_SRC = "import random\n_r = random.Random(7)\nARGS = ([_r.uniform(0, 1) for _ in range(3000)], 90)"


def gen(rng):
    xs = [rng.choice([rng.randint(-20, 20), rng.uniform(-20, 20)]) for _ in range(rng.randint(0, 12))]
    return (xs, rng.choice([0, 25, 50, 90, 99.5, 100, rng.uniform(0, 100), -1, 101]))


EDGES = [([], 50), ([1, 2], 50), ([1, 2, 3, 4], 25), ([5], 100), ([1, 3], 101)]


def fresh(seed):
    import random
    r = random.Random(seed)
    return ([r.uniform(0, 1) for _ in range(3000)], 90)
