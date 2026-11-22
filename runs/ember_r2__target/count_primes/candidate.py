from math import isqrt

def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= 2:
        return 0
    size = n // 2  # odd numbers 1,3,5,... < n; index i -> 2*i+1
    sieve = bytearray(b'\x01') * size
    sieve[0] = 0  # 1 is not prime
    limit = isqrt(n - 1)
    for p in range(3, limit + 1, 2):
        if sieve[p >> 1]:
            start = (p * p) >> 1
            step = p
            sieve[start:size:step] = b'\x00' * ((size - 1 - start) // step + 1)
    # +1 for the prime 2; sum(sieve) counts odd primes
    return 1 + sum(sieve)
