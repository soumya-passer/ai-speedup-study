_SMALL = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def _is_prime(n):
    if n < 2:
        return False
    for p in _SMALL:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while not d & 1:
        d >>= 1
        s += 1
    # deterministic bases: first 7 primes valid below 3.4e14, first 12 below 3.3e24
    bases = _SMALL[:7] if n < 341550071728321 else _SMALL
    for a in bases:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    return [_is_prime(n) for n in ns]
