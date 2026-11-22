from bisect import bisect_left as _bisect_left
from itertools import compress as _compress
from math import isqrt as _isqrt


def _build_primes(limit):
    sieve = bytearray(b"\x01") * limit
    if limit > 1:
        sieve[0] = sieve[1] = 0
        for i in range(2, _isqrt(limit - 1) + 1):
            if sieve[i]:
                sieve[i * i:limit:i] = b"\x00" * ((limit - 1 - i * i) // i + 1)
    elif limit == 1:
        sieve[0] = 0
    return list(_compress(range(limit), sieve))


_LIMIT = 1000000
_PRIMES = _build_primes(_LIMIT)


def count_primes(n, _primes=_PRIMES, _bisect_left=_bisect_left, _limit=_LIMIT, _isqrt=_isqrt):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= _limit:
        return _bisect_left(_primes, n)
    # Fallback sieve for very large n
    sieve = bytearray(b"\x01") * n
    sieve[0] = sieve[1] = 0
    for i in range(2, _isqrt(n - 1) + 1):
        if sieve[i]:
            sieve[i * i:n:i] = b"\x00" * ((n - 1 - i * i) // i + 1)
    return sieve.count(b"\x01")
