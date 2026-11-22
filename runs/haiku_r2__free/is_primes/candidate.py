_SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
# Bases 2..13 give a deterministic Miller-Rabin result for all n < 3,474,749,660,383.
_MR_BASES = (2, 3, 5, 7, 11, 13)


def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    out = []
    for n in ns:
        if n < 2:
            out.append(False)
            continue
        prime = True
        for p in _SMALL_PRIMES:
            if n % p == 0:
                prime = (n == p)
                break
        else:
            # n has no factor below 38, so every base above is smaller than n.
            d = n - 1
            s = 0
            while d % 2 == 0:
                d //= 2
                s += 1
            for a in _MR_BASES:
                x = pow(a, d, n)
                if x == 1 or x == n - 1:
                    continue
                for _ in range(s - 1):
                    x = x * x % n
                    if x == n - 1:
                        break
                else:
                    prime = False
                    break
        out.append(prime)
    return out
