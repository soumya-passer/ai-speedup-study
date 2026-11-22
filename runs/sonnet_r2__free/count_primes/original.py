def count_primes(n):
    """Number of primes p with 2 <= p < n. n is an int, may be 0 or negative."""
    count = 0
    for k in range(2, n):
        is_prime = True
        for d in range(2, k):
            if k % d == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count
