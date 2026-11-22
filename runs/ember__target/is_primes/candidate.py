def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    out = []
    append = out.append
    # Primes up to 100 for quick trial-division filtering.
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
             53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
    # First 12 prime bases are deterministic for
    # n < 318,665,857,834,031,151,167,461, far beyond 10**12 (and 2**64).
    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for n in ns:
        if n < 2:
            append(False)
            continue
        found = False
        for p in small:
            if n % p == 0:
                append(n == p)
                found = True
                break
        if found:
            continue
        # Miller-Rabin (deterministic in range above).
        # Remaining n > 97, so every base is < n.
        d = n - 1
        s = 0
        while not d & 1:
            d >>= 1
            s += 1
        is_prime = True
        for a in bases:
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                is_prime = False
                break
        append(is_prime)
    return out
