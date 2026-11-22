KIND = "trap"
TRAP = "a quick Fermat test calls numbers like 341 and 561 prime"
FUNC = "is_primes"
FLOAT_TOL = False

ORIGINAL = '''
def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    out = []
    for n in ns:
        if n < 2:
            out.append(False)
            continue
        if n % 2 == 0:
            out.append(n == 2)
            continue
        prime = True
        d = 3
        while d * d <= n:
            if n % d == 0:
                prime = False
                break
            d += 2
        out.append(prime)
    return out
'''

GOOD = '''
_BASES = (2, 3, 5, 7, 11, 13)


def _check(n):
    if n < 2:
        return False
    for p in _BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _BASES:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def is_primes(ns):
    return [_check(n) for n in ns]
'''

BAD = '''
def is_primes(ns):
    out = []
    for n in ns:
        if n < 4:
            out.append(n in (2, 3))
        elif n % 2 == 0:
            out.append(False)
        else:
            out.append(pow(2, n - 1, n) == 1)
    return out
'''

TESTS = [(([1, 2, 3, 4, 17, 18, 97],), [False, True, True, False, True, False, True]), (([],), [])]
BENCH_SRC = "import random\n_r = random.Random(7)\nARGS = ([_r.randint(10 ** 9, 10 ** 11) | 1 for _ in range(400)],)"

PSEUDO = [341, 561, 645, 1105, 1387, 1729, 1905, 2047, 2465, 2701, 2821, 3277, 4033, 4369, 4371,
          4681, 5461, 6601, 7957, 8321, 8481, 8911, 3215031751]


def gen(rng):
    out = []
    for _ in range(rng.randint(0, 8)):
        k = rng.random()
        if k < 0.3:
            out.append(rng.choice(PSEUDO))
        elif k < 0.4:
            out.append(rng.randint(-5, 5))
        else:
            out.append(rng.randint(0, 10 ** 6))
    return (out,)


EDGES = [([],), ([341, 561],), ([3215031751],), ([999999999989],), ([-7, 0, 1, 2],)]


def fresh(seed):
    import random
    r = random.Random(seed)
    return ([r.randint(10 ** 9, 10 ** 11) | 1 for _ in range(400)],)
