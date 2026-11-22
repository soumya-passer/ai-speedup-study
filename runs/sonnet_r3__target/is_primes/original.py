def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    out = []
    for n in ns:
        if n < 2:
            out.append(False)
            continue
        if n % 2 == 0:
            out.append(n == 2)
            continue
        prime = True
        d = 3
        while d * d <= n:
            if n % d == 0:
                prime = False
                break
            d += 2
        out.append(prime)
    return out
