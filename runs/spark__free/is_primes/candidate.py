import math as _math
_gcd = _math.gcd
_pow = pow
_M1 = 3*5*7*11*13*17*19*23*29*31*37*41*43*47
_M2 = 53*59*61*67*71*73*79*83*89*97
_S = frozenset((2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97))

def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    out = [False] * len(ns)
    gcd = _gcd
    pww = _pow
    M1 = _M1
    M2 = _M2
    S = _S
    for i, n in enumerate(ns):
        if n < 2:
            continue
        if (n & 1) == 0:
            if n == 2:
                out[i] = True
            continue
        if n <= 97:
            out[i] = n in S
            continue
        if gcd(n, M1) != 1 or gcd(n, M2) != 1:
            continue
        m = n - 1
        s = (m & -m).bit_length() - 1
        d = m >> s
        if n < 4759123141:
            # deterministic 2,7,61
            x = pww(2, d, n)
            if x != 1 and x != m:
                ss = s - 1
                while ss:
                    x = (x * x) % n
                    if x == m:
                        break
                    ss -= 1
                else:
                    continue
            x = pww(7, d, n)
            if x != 1 and x != m:
                ss = s - 1
                while ss:
                    x = (x * x) % n
                    if x == m:
                        break
                    ss -= 1
                else:
                    continue
            x = pww(61, d, n)
            if x != 1 and x != m:
                ss = s - 1
                while ss:
                    x = (x * x) % n
                    if x == m:
                        break
                    ss -= 1
                else:
                    continue
            out[i] = True
        else:
            # deterministic 2,13,23,1662803 for n < 1122004669633
            x = pww(2, d, n)
            if x != 1 and x != m:
                ss = s - 1
                while ss:
                    x = (x * x) % n
                    if x == m:
                        break
                    ss -= 1
                else:
                    continue
            x = pww(13, d, n)
            if x != 1 and x != m:
                ss = s - 1
                while ss:
                    x = (x * x) % n
                    if x == m:
                        break
                    ss -= 1
                else:
                    continue
            x = pww(23, d, n)
            if x != 1 and x != m:
                ss = s - 1
                while ss:
                    x = (x * x) % n
                    if x == m:
                        break
                    ss -= 1
                else:
                    continue
            x = pww(1662803, d, n)
            if x != 1 and x != m:
                ss = s - 1
                while ss:
                    x = (x * x) % n
                    if x == m:
                        break
                    ss -= 1
                else:
                    continue
            out[i] = True
    return out
