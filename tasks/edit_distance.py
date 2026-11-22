KIND = "control"
TRAP = "none - a 2-row table is fast and exact"
FUNC = "edit_distance"
FLOAT_TOL = False

ORIGINAL = '''
def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
    return d[n][m]
'''

GOOD = '''
def edit_distance(a, b):
    # Myers / Hyyro bit-parallel method: one table column per Python int
    if not a:
        return len(b)
    if not b:
        return len(a)
    m = len(a)
    full = (1 << m) - 1
    top = 1 << (m - 1)
    peq = {}
    for i, c in enumerate(a):
        peq[c] = peq.get(c, 0) | (1 << i)
    pv, mv, score = full, 0, m
    for c in b:
        eq = peq.get(c, 0)
        xv = eq | mv
        xh = (((eq & pv) + pv) ^ pv) | eq
        ph = mv | ~(xh | pv)
        mh = pv & xh
        if ph & top:
            score += 1
        elif mh & top:
            score -= 1
        ph = ((ph << 1) | 1) & full
        mh = (mh << 1) & full
        pv = (mh | ~(xv | ph)) & full
        mv = ph & xv
    return score
'''

BAD = None

TESTS = [(("kitten", "sitting"), 3), (("", "abc"), 3)]
BENCH_SRC = "import random\n_r = random.Random(7)\nARGS = (''.join(_r.choice('acgt') for _ in range(500)), ''.join(_r.choice('acgt') for _ in range(500)))"


def gen(rng):
    al = rng.choice(["ab", "acgt", "abcxyz", "aéß "])
    return ("".join(rng.choice(al) for _ in range(rng.randint(0, 12))),
            "".join(rng.choice(al) for _ in range(rng.randint(0, 12))))


EDGES = [("", ""), ("a", ""), ("", "b"), ("same", "same")]


def fresh(seed):
    import random
    r = random.Random(seed)
    return ("".join(r.choice("acgt") for _ in range(500)), "".join(r.choice("acgt") for _ in range(500)))
