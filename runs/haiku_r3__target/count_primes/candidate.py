def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= 2:
        return 0
    # Sieve of Eratosthenes over 0..n-1: sieve[i] is 1 if i is prime.
    sieve = bytearray([1]) * n
    sieve[0] = 0
    sieve[1] = 0
    i = 2
    while i * i < n:
        if sieve[i]:
            sieve[i * i::i] = bytes(len(range(i * i, n, i)))
        i += 1
    return sum(sieve)
