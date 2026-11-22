KIND = "trap"
TRAP = "changing the caller's list in place, or dividing by zero when all values are equal"
FUNC = "normalize"
FLOAT_TOL = False

ORIGINAL = '''
def normalize(xs):
    """Scale numbers to the range 0 to 1: (x - min) / (max - min).
    If all values are equal, every result is 0.0. An empty list gives [].
    Returns a new list; the input list must not change."""
    out = []
    for x in xs:
        lo = min(xs)
        hi = max(xs)
        if hi == lo:
            out.append(0.0)
        else:
            out.append((x - lo) / (hi - lo))
    return out
'''

GOOD = '''
def normalize(xs):
    if not xs:
        return []
    lo = min(xs)
    hi = max(xs)
    if hi == lo:
        return [0.0] * len(xs)
    span = hi - lo
    return [(x - lo) / span for x in xs]
'''

BAD = '''
def normalize(xs):
    lo, hi = (min(xs), max(xs)) if xs else (0, 1)
    for i, x in enumerate(xs):
        xs[i] = (x - lo) / (hi - lo)
    return xs
'''

TESTS = [(([0, 5, 10],), [0.0, 0.5, 1.0]), (([2.0, 4.0],), [0.0, 1.0])]
BENCH_SRC = "import random\n_r = random.Random(7)\nARGS = ([_r.uniform(-50, 50) for _ in range(3000)],)"


def gen(rng):
    size = rng.randint(0, 12)
    if rng.random() < 0.3:
        v = rng.uniform(-5, 5)
        return ([v] * size,)
    return ([rng.choice([rng.randint(-5, 5), rng.uniform(-5, 5)]) for _ in range(size)],)


EDGES = [([],), ([3.0],), ([7, 7, 7],), ([1, 2],)]


def fresh(seed):
    import random
    r = random.Random(seed)
    return ([r.uniform(-50, 50) for _ in range(3000)],)
