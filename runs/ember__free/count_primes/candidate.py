from math import isqrt


def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= 2:
        return 0
    # Odd-only sieve: index i represents the odd number 2*i + 1.
    # size = number of odds < n (1, 3, 5, ...). The even prime 2 is
    # counted separately in the final +1.
    size = n // 2
    sieve = bytearray(b"\x01") * size
    sieve[0] = 0  # 1 is not prime
    limit = isqrt(n - 1)
    for i in range(3, limit + 1, 2):
        if sieve[i // 2]:
            # Mark i*i, i*i + 2i, i*i + 4i, ...  In index space
            # (number = 2*index + 1) this is start, start+i, start+2i, ...
            start = (i * i - 1) // 2
            sieve[start::i] = b"\x00" * ((size - 1 - start) // i + 1)
    # 1 for the prime 2, plus the remaining unmarked odds.
    return 1 + sieve.count(b"\x01")
