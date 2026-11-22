def word_wrap(text, width):
    """Greedy wrap. Words are separated only by the space character; tabs,
    new lines and hyphens are part of a word. Each line holds as many words
    as fit within width, joined by one space. A word longer than width is
    cut into pieces of width characters, each on its own line, and the last
    piece starts the next line. Raises ValueError when width < 1."""
    if width < 1:
        raise ValueError("width < 1")
    lines = []
    lappend = lines.append
    cur = []
    cappend = cur.append
    cclear = cur.clear
    cur_len = 0
    W = width
    for w in text.split(" "):
        if not w:
            continue
        lw = len(w)
        if lw > W:
            if cur_len:
                lappend(" ".join(cur))
                cclear()
                cur_len = 0
            # emit full-width chunks directly
            nfull = (lw - 1) // W
            start = 0
            # local bind for slice loop
            for _ in range(nfull):
                lappend(w[start:start + W])
                start += W
            w = w[start:]
            lw -= start
            cappend(w)
            cur_len = lw
            continue
        if cur_len == 0:
            cappend(w)
            cur_len = lw
        else:
            nl = cur_len + 1 + lw
            if nl <= W:
                cappend(w)
                cur_len = nl
            else:
                lappend(" ".join(cur))
                cclear()
                cappend(w)
                cur_len = lw
    if cur_len:
        lappend(" ".join(cur))
    return lines
