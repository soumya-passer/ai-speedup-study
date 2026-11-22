import math

def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= 2:
        return 0
    # Odd-only Sieve of Eratosthenes.
    # sieve[i] corresponds to number 2*i+1, i in [0, n//2).
    # Index 0 is number 1 (not prime). Prime 2 counted separately.
    size = n // 2
    sieve = bytearray(b'\x01') * size
    sieve[0] = 0
    limit = (math.isqrt(n) - 1) // 2
    for i in range(1, limit + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p - 1) // 2
            step = p
            sieve[start:size:step] = b'\x00' * ((size - 1 - start) // step + 1)
    # sieve.count is implemented in C, faster than sum()
    return 1 + sieve.count(1)
