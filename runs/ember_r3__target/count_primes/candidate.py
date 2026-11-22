def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= 2:
        return 0
    sieve = bytearray(b"\x01") * n
    sieve[0] = 0
    sieve[1] = 0
    limit = int(n ** 0.5)
    for i in range(2, limit + 1):
        if sieve[i]:
            start = i * i
            sieve[start:n:i] = b"\x00" * ((n - 1 - start) // i + 1)
    return sum(sieve)
