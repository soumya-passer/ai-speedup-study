def word_wrap(text, width):
    """Greedy wrap. Words are separated only by the space character; tabs,
    new lines and hyphens are part of a word. Each line holds as many words
    as fit within width, joined by one space. A word longer than width is
    cut into pieces of width characters, each on its own line, and the last
    piece starts the next line. Raises ValueError when width < 1."""
    if width < 1:
        raise ValueError("width < 1")
    lines = []
    lines_append = lines.append
    join = " ".join
    cur = []
    cur_append = cur.append
    # cur_len is length of " ".join(cur), or -1 when cur is empty.
    # The -1 sentinel lets the common "add to current line" test work
    # uniformly: -1 + 1 + lw == lw <= width for an empty line.
    cur_len = -1
    for w in text.split(" "):
        if not w:
            continue
        lw = len(w)
        if lw > width:
            if cur_len >= 0:
                lines_append(join(cur))
                cur.clear()
                cur_len = -1
            start = 0
            while lw - start > width:
                lines_append(w[start:start + width])
                start += width
            w = w[start:]
            lw -= start
        if cur_len + 1 + lw <= width:
            cur_append(w)
            cur_len += 1 + lw
        else:
            lines_append(join(cur))
            cur.clear()
            cur_append(w)
            cur_len = lw
    if cur_len >= 0:
        lines_append(join(cur))
    return lines
