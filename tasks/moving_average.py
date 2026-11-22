KIND = "trap"
TRAP = "sum() or a running total changes float results; the spec demands bit-identical output"
FUNC = "moving_average"
FLOAT_TOL = False  # spec says bit-identical

ORIGINAL = '''
def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    out = []
    for i in range(len(xs) - w + 1):
        total = 0.0
        for j in range(i, i + w):
            total = total + float(xs[j]) * 1.0
        out.append(total / w)
    return out
'''

GOOD = '''
def moving_average(xs, w):
    if w < 1:
        raise ValueError("w < 1")
    xs = [float(x) for x in xs]
    out = []
    for i in range(len(xs) - w + 1):
        total = 0.0
        for v in xs[i:i + w]:
            total += v
        out.append(total / w)
    return out
'''

BAD = '''
def moving_average(xs, w):
    if w < 1:
        raise ValueError("w < 1")
    return [sum(xs[i:i + w], 0.0) / w for i in range(len(xs) - w + 1)]
'''

TESTS = [(([1.0, 2.0, 3.0, 4.0], 2), [1.5, 2.5, 3.5]), (([1.0], 3), [])]
BENCH_SRC = "import random\n_r = random.Random(7)\nARGS = ([_r.uniform(0, 1) for _ in range(3000)], 300)"


def gen(rng):
    size = rng.randint(0, 30)
    if rng.random() < 0.5:
        xs = [rng.uniform(-100, 100) for _ in range(size)]
    else:
        xs = [rng.choice([1e16, -1e16, 1.0, 0.1, 3.3]) for _ in range(size)]
    return (xs, rng.randint(-1, 8))


EDGES = [([], 1), ([1.0], 0), ([0.1, 0.2, 0.3], 3), ([1e16, 1.0, -1e16], 3)]


def fresh(seed):
    import random
    r = random.Random(seed)
    return ([r.uniform(0, 1) for _ in range(3000)], 300)
