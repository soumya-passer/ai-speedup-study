def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= 2:
        return 0
    sieve = bytearray([1]) * n
    sieve[0] = sieve[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(range(i * i, n, i)))
    return sum(sieve)
