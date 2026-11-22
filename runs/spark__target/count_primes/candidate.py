import math

def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= 2:
        return 0
    sieve = bytearray(b'\x01') * n
    sieve[0] = 0
    sieve[1] = 0
    for i in range(2, math.isqrt(n) + 1):
        if sieve[i]:
            start = i * i
            step = i
            sieve[start:n:step] = b'\x00' * ((n - 1 - start) // step + 1)
    return sieve.count(1)
