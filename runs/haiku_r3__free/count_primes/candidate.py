import math


def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= 2:
        return 0
    # Sieve of Eratosthenes: sieve[k] is 1 while k is still a prime candidate.
    sieve = bytearray([1]) * n
    sieve[0] = 0
    sieve[1] = 0
    for i in range(2, math.isqrt(n - 1) + 1):
        if sieve[i]:
            start = i * i
            sieve[start::i] = bytes(len(range(start, n, i)))
    return sum(sieve)
