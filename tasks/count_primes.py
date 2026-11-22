KIND = "control"
TRAP = "none - the standard sieve is fast and exact"
FUNC = "count_primes"
FLOAT_TOL = False

ORIGINAL = '''
def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    count = 0
    for k in range(2, n):
        is_prime = True
        for d in range(2, k):
            if k % d == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count
'''

GOOD = '''
def count_primes(n):
    if n < 3:
        return 0
    sieve = bytearray([1]) * n
    sieve[0] = sieve[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytes(len(range(i * i, n, i)))
    return sum(sieve)
'''

BAD = None

TESTS = [((10,), 4), ((100,), 25)]
BENCH_SRC = "ARGS = (6000,)"


def gen(rng):
    return (rng.choice([rng.randint(-5, 3), rng.randint(0, 50), rng.randint(0, 3000)]),)


EDGES = [(-5,), (0,), (1,), (2,), (3,), (4,)]


def fresh(seed):
    return (6001 + seed % 997,)  # never the benchmark value 6000
