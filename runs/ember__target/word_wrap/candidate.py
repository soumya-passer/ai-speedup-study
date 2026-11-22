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
    cur = []
    cur_len = 0
    for w in text.split(" "):
        if not w:
            continue
        lw = len(w)
        if lw > width:
            if cur:
                lines_append(" ".join(cur))
            pos = 0
            while lw - pos > width:
                lines_append(w[pos:pos + width])
                pos += width
            cur = [w[pos:]]
            cur_len = lw - pos
            continue
        if cur_len == 0:
            cur = [w]
            cur_len = lw
        elif cur_len + 1 + lw <= width:
            cur.append(w)
            cur_len += 1 + lw
        else:
            lines_append(" ".join(cur))
            cur = [w]
            cur_len = lw
    if cur:
        lines_append(" ".join(cur))
    return lines
