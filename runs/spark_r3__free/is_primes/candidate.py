def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    out = []
    ap = out.append
    # Deterministic Miller-Rabin for n < 2,152,302,897,847 (covers 1e12):
    # bases 2,3,5,7,11. Unrolled for speed.
    for n in ns:
        if n < 2:
            ap(False)
            continue
        if (n & 1) == 0:
            ap(n == 2)
            continue
        if n % 3 == 0:
            ap(n == 3)
            continue
        if n % 5 == 0:
            ap(n == 5)
            continue
        if n % 7 == 0:
            ap(n == 7)
            continue
        if n < 121:
            ap(True)
            continue
        if n % 11 == 0 or n % 13 == 0 or n % 17 == 0 or n % 19 == 0 or n % 23 == 0 or n % 29 == 0 or n % 31 == 0 or n % 37 == 0:
            ap(False)
            continue
        if n % 41 == 0 or n % 43 == 0 or n % 47 == 0 or n % 53 == 0 or n % 59 == 0 or n % 61 == 0 or n % 67 == 0 or n % 71 == 0:
            ap(False)
            continue
        if n % 73 == 0 or n % 79 == 0 or n % 83 == 0 or n % 89 == 0 or n % 97 == 0:
            ap(False)
            continue
        if n < 10201:
            ap(True)
            continue
        d = (n - 1) >> 1
        s = 1
        while (d & 1) == 0:
            d >>= 1
            s += 1
        nm1 = n - 1
        x = pow(2, d, n)
        if x != 1 and x != nm1:
            for _ in range(s - 1):
                x = (x * x) % n
                if x == nm1:
                    break
            else:
                ap(False)
                continue
        x = pow(3, d, n)
        if x != 1 and x != nm1:
            for _ in range(s - 1):
                x = (x * x) % n
                if x == nm1:
                    break
            else:
                ap(False)
                continue
        x = pow(5, d, n)
        if x != 1 and x != nm1:
            for _ in range(s - 1):
                x = (x * x) % n
                if x == nm1:
                    break
            else:
                ap(False)
                continue
        x = pow(7, d, n)
        if x != 1 and x != nm1:
            for _ in range(s - 1):
                x = (x * x) % n
                if x == nm1:
                    break
            else:
                ap(False)
                continue
        x = pow(11, d, n)
        if x != 1 and x != nm1:
            for _ in range(s - 1):
                x = (x * x) % n
                if x == nm1:
                    break
            else:
                ap(False)
                continue
        ap(True)
    return out
