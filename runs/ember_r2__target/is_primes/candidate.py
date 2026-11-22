def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    out = []
    append = out.append
    small_primes = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    # Deterministic Miller-Rabin for n < 10**12 (in fact far beyond):
    # testing prime bases 2..37 is deterministic well past 3.4e12.
    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    _pow = pow
    for n in ns:
        if n < 2:
            append(False)
            continue
        if n % 2 == 0:
            append(n == 2)
            continue
        # Small-prime trial division: resolves all n <= 37 and many composites.
        resolved = False
        for p in small_primes:
            if n % p == 0:
                append(n == p)
                resolved = True
                break
        if resolved:
            continue
        # Now n > 37, odd, and not divisible by any prime <= 37, so all bases < n.
        # Write n - 1 = d * 2**s with d odd.
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        prime = True
        for a in bases:
            x = _pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                prime = False
                break
        append(prime)
    return out
