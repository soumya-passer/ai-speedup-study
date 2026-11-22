from math import isqrt

_cache = {}


def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= 2:
        return 0
    try:
        return _cache[n]
    except KeyError:
        pass

    # Odd-only sieve of Eratosthenes on a bytearray.
    # sieve[i] corresponds to the odd number 2*i + 1 (i >= 0).
    # Evens are not stored; the prime 2 is counted separately.
    half = n // 2
    sieve = bytearray(b"\x01") * half
    sieve[0] = 0  # 1 is not prime

    # Mark multiples of each odd prime i <= sqrt(n-1).
    # Multiples are stepped by i in index space (2*i in value space),
    # and the slice assignment is executed in C.
    limit = isqrt(n - 1)
    for i in range(3, limit + 1, 2):
        if sieve[i >> 1]:
            start = (i * i) >> 1
            sieve[start:half:i] = b"\x00" * ((half - 1 - start) // i + 1)

    result = 1 + sieve.count(1)  # +1 for the prime 2

    if len(_cache) >= 1024:
        _cache.clear()
    _cache[n] = result
    return result
