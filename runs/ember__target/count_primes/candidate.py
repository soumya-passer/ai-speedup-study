def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    if n <= 2:
        return 0
    # Odd-only sieve: index i represents number 2*i+1 (i=0 -> 1, i=1 -> 3, ...)
    size = n // 2  # odd numbers < n are 1,3,5,...,2*size-1
    sieve = bytearray(b"\x01") * size
    sieve[0] = 0  # 1 is not prime
    # Only need to sieve primes p with p*p < n
    limit = int(n ** 0.5) + 1
    # i from 1 -> p=3 upward
    for i in range(1, (limit // 2) + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p) // 2  # index of p*p
            step = p
            # Slice assignment in C marks all multiples of p
            sieve[start::step] = b"\x00" * ((size - 1 - start) // step + 1)
    # 1 for prime 2, plus odd primes
    return 1 + sum(sieve)
