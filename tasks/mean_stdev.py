KIND = "trap"
TRAP = "one-pass sum-of-squares formula loses all precision when values are large and close together"
FUNC = "mean_stdev"
FLOAT_TOL = True

ORIGINAL = '''
def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    This version works in exact fractions, so it is as accurate as possible.
    Floats may differ from this function only by rounding (relative 1e-6).
    Raises ValueError on an empty list."""
    from fractions import Fraction
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    exact = [Fraction(x) for x in xs]
    mean = sum(exact) / n
    var = sum((x - mean) ** 2 for x in exact) / n
    return (float(mean), float(var) ** 0.5)
'''

GOOD = '''
def mean_stdev(xs):
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    mean = sum(xs, 0.0) / n
    sq = sum([(x - mean) * (x - mean) for x in xs], 0.0)
    return (mean, (sq / n) ** 0.5)
'''

BAD = '''
def mean_stdev(xs):
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    s = sum(xs, 0.0)
    s2 = sum([x * x for x in xs], 0.0)
    mean = s / n
    var = s2 / n - mean * mean
    return (mean, abs(var) ** 0.5)
'''

TESTS = [(([2, 4, 4, 4, 5, 5, 7, 9],), (5.0, 2.0)), (([1.0],), (1.0, 0.0))]
BENCH_SRC = "import random\n_r = random.Random(7)\nARGS = ([_r.uniform(0, 100) for _ in range(50000)],)"


def gen(rng):
    size = rng.randint(1, 40)
    k = rng.random()
    if k < 0.4:
        xs = [rng.uniform(-100, 100) for _ in range(size)]
    elif k < 0.8:  # large values close together
        base = rng.choice([1e6, 1e7, 1e8])
        xs = [base + rng.uniform(0, 1) for _ in range(size)]
    else:
        xs = [rng.randint(-10, 10) for _ in range(size)]
    return (xs,)


EDGES = [([],), ([5.0, 5.0, 5.0],), ([1e9 + 0.1, 1e9 + 0.2, 1e9 + 0.3],)]


def fresh(seed):
    import random
    r = random.Random(seed)
    return ([r.uniform(0, 100) for _ in range(50000)],)
