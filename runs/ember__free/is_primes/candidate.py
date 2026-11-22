from math import gcd

_SMALL_PRIMES = frozenset(
    (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
     53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
)
# Product of all primes <= 47.  gcd(n, _P47) != 1 (for n > 47) means
# n is divisible by a small prime, hence composite.  One C-level gcd
# eliminates ~86% of random composites.
_P47 = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31 * 37 * 41 * 43 * 47

# Deterministic Miller-Rabin bases:
#  - n < 2,152,302,898,747 (smallest strong pseudoprime to 2,3,5,7,11):
#    bases 2, 3, 5, 7, 11 are sufficient (covers the documented < 10**12).
#  - larger n: first 12 prime bases, deterministic well beyond 2**64 range
#    for practical purposes / at least same set used for < 2**64 in tables.
_BASES_SMALL = (2, 3, 5, 7, 11)
_BASES_LARGE = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
_LIMIT5 = 2152302898747


def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    out = []
    append = out.append
    small = _SMALL_PRIMES
    p47 = _P47
    bases_small = _BASES_SMALL
    bases_large = _BASES_LARGE
    limit = _LIMIT5
    _gcd = gcd

    for n in ns:
        if n < 100:
            append(n in small)
            continue
        # n >= 100 > 47, so a common factor with _P47 proves compositeness
        if _gcd(n, p47) != 1:
            append(False)
            continue

        # Deterministic Miller-Rabin.  n is odd here (otherwise gcd above
        # would be >= 2), so n - 1 is even and s >= 1.
        d = n - 1
        s = (d & -d).bit_length() - 1
        d >>= s
        prime = True
        for a in (bases_small if n < limit else bases_large):
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                prime = False
                break
        append(prime)
    return out
