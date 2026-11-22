"""Fast deterministic Miller-Rabin primality test.

Deterministic for n < 1e12 (and, with tiered bases, for all n < 2**64)
using known bounds, plus trial division by small primes.
"""

_SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)

_BASES_1 = (2, 3, 5, 7, 11)                                   # n < 2_152_302_898_747
_BASES_2 = (2, 3, 5, 7, 11, 13, 17, 19, 23)                   # n < 3_825_123_056_546_413_051
_BASES_64 = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)  # n < 2**64


def _is_prime(n):
    if n < 2:
        return False
    # Trial division by small primes; also completes the test for
    # n <= 97*97, where p*p > n proves primality.
    for p in _SMALL_PRIMES:
        if p * p > n:
            return True
        if n % p == 0:
            return n == p

    # Miller-Rabin: write n-1 = d * 2**s with d odd.
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    if n < 2152302898747:
        bases = _BASES_1
    elif n < 3825123056546413051:
        bases = _BASES_2
    else:
        bases = _BASES_64

    n_minus_1 = n - 1
    for a in bases:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n_minus_1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n_minus_1:
                break
        else:
            return False
    return True


def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    return [_is_prime(n) for n in ns]
