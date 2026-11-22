import math as _m
_gcd = _m.gcd
# product of odd primes 3..47 and 53..97 (both < 2**62)
_P1 = 614889782588491410
_P2 = 32589158477190044730 % (1 << 62)
# recompute exactly to avoid mistake
_P1 = 3*5*7*11*13*17*19*23*29*31*37*41*43*47
_P2 = 53*59*61*67*71*73*79*83*89*97
_SSET = frozenset((3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97))

def is_primes(ns):
    """For each int n below 10**12, True if n is prime, else False.
    Negative numbers, 0 and 1 are not prime."""
    out = []
    ap = out.append
    gcd = _gcd
    P1 = _P1
    P2 = _P2
    SSET = _SSET
    _pow = pow
    for n in ns:
        if n < 2:
            ap(False)
            continue
        if not (n & 1):
            ap(n == 2)
            continue
        if n <= 97:
            ap(n in SSET)
            continue
        if gcd(n, P1) != 1 or gcd(n, P2) != 1:
            ap(False)
            continue
        m = n - 1
        s = ((m & -m).bit_length() - 1)
        d = m >> s
        nm1 = m
        # deterministic MR for n < 2_152_302_898_747, bases 2,3,5,7,11
        x = _pow(2, d, n)
        if x != 1 and x != nm1:
            y = s - 1
            while True:
                x = (x * x) % n
                if x == nm1:
                    break
                y -= 1
                if not y:
                    ap(False)
                    break
            else:
                pass
            if y == 0 and x != nm1:
                continue
            # need to check y==0 case handled: if broke via y==0 falsely?
            # redo logic cleanly below is tricky; use flag approach
            # To keep it simple and fast, fall through only if not composite.
            # We used break/continue; verify:
            # if inner found nm1 -> break -> continue outer base checks
            # if exhausted -> ap(False) + break -> need to skip to next n
            # Detect exhaustion: x != nm1 after loop
            if x != nm1:
                continue
        x = _pow(3, d, n)
        if x != 1 and x != nm1:
            y = s - 1
            while True:
                x = (x * x) % n
                if x == nm1:
                    break
                y -= 1
                if not y:
                    ap(False)
                    break
            if x != nm1:
                continue
        x = _pow(5, d, n)
        if x != 1 and x != nm1:
            y = s - 1
            while True:
                x = (x * x) % n
                if x == nm1:
                    break
                y -= 1
                if not y:
                    ap(False)
                    break
            if x != nm1:
                continue
        x = _pow(7, d, n)
        if x != 1 and x != nm1:
            y = s - 1
            while True:
                x = (x * x) % n
                if x == nm1:
                    break
                y -= 1
                if not y:
                    ap(False)
                    break
            if x != nm1:
                continue
        x = _pow(11, d, n)
        if x != 1 and x != nm1:
            y = s - 1
            while True:
                x = (x * x) % n
                if x == nm1:
                    break
                y -= 1
                if not y:
                    ap(False)
                    break
            if x != nm1:
                continue
        ap(True)
    return out
