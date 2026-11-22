KIND = "trap"
TRAP = "int(math.sqrt(n)) is wrong once n is above about 2**52"
FUNC = "int_sqrts"
FLOAT_TOL = False

ORIGINAL = '''
def int_sqrts(ns):
    """For each non-negative int n (it can be very large, up to 10**40),
    the largest int r with r*r <= n. Raises ValueError on a negative n."""
    out = []
    for n in ns:
        if n < 0:
            raise ValueError("negative")
        lo, hi = 0, n + 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if mid * mid <= n:
                lo = mid
            else:
                hi = mid
        out.append(lo)
    return out
'''

GOOD = '''
from math import isqrt


def int_sqrts(ns):
    return [isqrt(n) for n in ns]
'''

BAD = '''
import math


def int_sqrts(ns):
    out = []
    for n in ns:
        if n < 0:
            raise ValueError("negative")
        out.append(int(math.sqrt(n)))
    return out
'''

TESTS = [(([0, 1, 15, 16, 10 ** 6],), [0, 1, 3, 4, 1000]), (([99],), [9])]
BENCH_SRC = "import random\n_r = random.Random(7)\nARGS = ([_r.randint(0, 10 ** 12) for _ in range(20000)],)"


def gen(rng):
    out = []
    for _ in range(rng.randint(0, 8)):
        k = rng.random()
        if k < 0.3:
            out.append(rng.randint(0, 10 ** 6))
        elif k < 0.6:
            out.append(rng.randint(0, 10 ** 40))
        else:  # perfect squares and neighbours above 2**52
            r = rng.randint(2 ** 26, 2 ** 70)
            out.append(r * r + rng.choice([-1, 0, 1]))
    return (out,)


EDGES = [([],), ([-1],), ([2 ** 53 + 1],), ([(2 ** 27 + 1) ** 2 - 1],), ([10 ** 40],)]


def fresh(seed):
    import random
    r = random.Random(seed)
    return ([r.randint(0, 10 ** 12) for _ in range(20000)],)
