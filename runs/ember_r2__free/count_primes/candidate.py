from math import isqrt


def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= 2:
        return 0
    # Odd-only sieve of Eratosthenes.
    # sieve[i] corresponds to the odd number 2*i + 1 (< n), so there are
    # n // 2 entries.  Even numbers (except the prime 2) are never stored.
    size = n // 2
    sieve = bytearray(b"\x01") * size
    sieve[0] = 0  # 1 is not prime
    limit = isqrt(n - 1)  # largest p with p * p < n
    # Only odd p can be prime > 2; marking odd multiples of p steps by
    # 2*p in value, i.e. by p in index space.  Slice assignment is
    # performed in C, so the inner marking loops are very fast.
    for p in range(3, limit + 1, 2):
        if sieve[p // 2]:
            start = p * p
            start_idx = start // 2
            sieve[start_idx:size:p] = b"\x00" * ((size - 1 - start_idx) // p + 1)
    # +1 accounts for the prime 2; count() is implemented in C.
    return sieve.count(1) + 1
