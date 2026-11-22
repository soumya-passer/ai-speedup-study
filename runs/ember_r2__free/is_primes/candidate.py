_SMALL = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def _is_prime(n):
    if n < 2:
        return False
    for p in _SMALL:
        if n % p == 0:
            return n == p
    # n is coprime to first 12 primes; below 37**2 it must be prime.
    if n < 1369:
        return True
    # Deterministic Miller-Rabin for n < 318,665,857,834,031,151,167,461
    # (in particular for all n < 10**12 and all 64-bit n) using the
    # first 12 prime bases 2..37.  pow() is implemented in C.
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    nm1 = n - 1
    for a in _SMALL:
        x = pow(a, d, n)
        if x == 1 or x == nm1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == nm1:
                break
        else:
            return False
    return True


def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    return [_is_prime(n) for n in ns]
