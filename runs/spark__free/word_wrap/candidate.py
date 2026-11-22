def word_wrap(text, width):
    if width < 1:
        raise ValueError("width < 1")
    if not text:
        return []
    lines = []
    la = lines.append
    js = " ".join
    cur = []
    ca = cur.append
    cl = cur.clear
    cur_len = -1
    for w in text.split(" "):
        lw = len(w)
        if not lw:
            continue
        nlen = cur_len + 1 + lw
        if nlen <= width:
            ca(w)
            cur_len = nlen
            continue
        if cur:
            la(js(cur))
            cl()
        if lw <= width:
            ca(w)
            cur_len = lw
        else:
            pos = 0
            # cut into width-sized pieces
            # manual loop, long words are rare
            while lw - pos > width:
                la(w[pos:pos + width])
                pos += width
            last = w[pos:]
            ca(last)
            cur_len = lw - pos
    if cur:
        la(js(cur))
    return lines
