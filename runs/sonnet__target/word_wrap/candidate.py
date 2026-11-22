def word_wrap(text, width):
    """Greedy wrap. Words are separated only by the space character; tabs,
    new lines and hyphens are part of a word. Each line holds as many words
    as fit within width, joined by one space. A word longer than width is
    cut into pieces of width characters, each on its own line, and the last
    piece starts the next line. Raises ValueError when width < 1."""
    if width < 1:
        raise ValueError("width < 1")
    lines = []
    append = lines.append
    cur = []
    cur_append = cur.append
    n = 0  # length of the joined current line
    for w in text.split(" "):
        if not w:
            continue
        lw = len(w)
        if lw > width:
            if cur:
                append(" ".join(cur))
                cur = []
                cur_append = cur.append
            while lw > width:
                append(w[:width])
                w = w[width:]
                lw -= width
        if cur:
            if n + 1 + lw <= width:
                cur_append(w)
                n += 1 + lw
            else:
                append(" ".join(cur))
                cur = [w]
                cur_append = cur.append
                n = lw
        else:
            cur = [w]
            cur_append = cur.append
            n = lw
    if cur:
        append(" ".join(cur))
    return lines
