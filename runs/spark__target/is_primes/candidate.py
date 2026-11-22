def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    SMALL = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    # Deterministic Miller-Rabin for n < 2152302898747 (covers n < 1e12):
    # bases 2,3,5,7,11 suffice. Add 13 for extra margin (still cheap).
    BASES = (2, 3, 5, 7, 11, 13)
    out = [False] * len(ns)
    for i, n in enumerate(ns):
        if n < 2:
            continue
        # quick trial division by small primes
        div_found = False
        for p in SMALL:
            if n % p == 0:
                out[i] = (n == p)
                div_found = True
                break
        if div_found:
            continue
        # write n-1 = d * 2**s with d odd
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        nm1 = n - 1
        is_p = True
        for a in BASES:
            # a < n here since n > 37 >= a, so no need for a % n case
            x = pow(a, d, n)
            if x == 1 or x == nm1:
                continue
            for _ in range(s - 1):
                x = (x * x) % n
                if x == nm1:
                    break
            else:
                is_p = False
                break
        out[i] = is_p
    return out
