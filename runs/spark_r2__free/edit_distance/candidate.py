def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if lb == 0:
        return la
    if la == 0:
        return lb
    if la < lb:
        a, b = b, a
        la, lb = lb, la
    m = lb
    pe = {}
    for i, ch in enumerate(b):
        pe[ch] = pe.get(ch, 0) | (1 << i)
    mask = (1 << m) - 1
    top = 1 << (m - 1)
    vp = mask
    vn = 0
    curr = m
    pe_get = pe.get
    for ch in a:
        eq = pe_get(ch, 0)
        x = eq | vn
        d0 = ((((x & vp) + vp) & mask) ^ vp) | x
        hn = d0 & vp
        hp = (vn | ~(d0 | vp)) & mask
        if hp & top:
            curr += 1
        elif hn & top:
            curr -= 1
        hp = ((hp << 1) | 1) & mask
        hn = (hn << 1) & mask
        vp = (hn | ~(d0 | hp)) & mask
        vn = hp & d0
    return curr
