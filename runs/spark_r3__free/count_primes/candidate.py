import math as _math
_isqrt = _math.isqrt
_cache = {}

def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    try:
        return _cache[n]
    except KeyError:
        pass
    if n <= 2:
        return 0
    size = n // 2
    s = bytearray(b'\x01') * size
    s[0] = 0
    lim = _isqrt(n) + 1
    # mark multiples of odd primes; s[i] <=> 2*i+1 is prime
    for p in range(3, lim, 2):
        if s[p >> 1]:
            start = (p * p) >> 1
            step = p
            s[start::step] = b'\x00' * ((size - 1 - start) // step + 1)
    r = s.count(1) + 1
    _cache[n] = r
    return r
