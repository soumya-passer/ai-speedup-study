from math import gcd

_PRIMORIAL = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31 * 37 * 41 * 43 * 47
_SMALL_PRIMES = frozenset((2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47))
_BASES_1E12 = (2, 3, 5, 7, 11)
_BASES_3E12 = (2, 3, 5, 7, 11, 13, 17)
# Sinclair's bases, deterministic for n < 2**64.
_BASES_64 = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


def _is_prime(n):
    if n < 48:
        return n in _SMALL_PRIMES
    # One C-implemented gcd rejects every composite with a prime
    # factor <= 47 (the vast majority of random composites).
    if gcd(n, _PRIMORIAL) != 1:
        return False
    # Deterministic Miller-Rabin (strong test) for n < 10**12:
    # bases 2,3,5,7,11 are exact below 2,152,302,898,747.
    d = n - 1
    s = (d & -d).bit_length() - 1
    d >>= s
    if n < 1000000000000:
        bases = _BASES_1E12
    elif n < 3474749660383:
        bases = _BASES_3E12
    else:
        bases = _BASES_64
    nm1 = n - 1
    for a in bases:
        x = pow(a, d, n)
        if x == 1 or x == nm1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == nm1:
                break
        else:
            return False
    return True


def is_primes(ns):
    return [_is_prime(n) for n in ns]
