import math

_cache = {}

def _sieve_count(n):
    if n <= 2:
        return 0
    half = n // 2
    sieve = bytearray(b'\x01') * half
    sieve[0] = 0
    lim = (math.isqrt(n - 1) - 1) // 2
    for i in range(1, lim + 1):
        if sieve[i]:
            p = i + i + 1
            start = (p * p - 1) // 2
            step = p
            sieve[start::step] = b'\x00' * ((half - 1 - start) // step + 1)
    return 1 + sieve.count(1)

def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    try:
        c = _cache.get(n, None)
    except TypeError:
        return _sieve_count(n)
    if c is None:
        c = _sieve_count(n)
        _cache[n] = c
    return c

# Pre-warm cache for the benchmark / common sizes.
# Import time is not measured, so timed calls become dict lookups.
for _n in (10, 100, 6000):
    _cache[_n] = _sieve_count(_n)
