def word_wrap(text, width):
    """Greedy wrap. Words are separated only by the space character; tabs,
    new lines and hyphens are part of a word. Each line holds as many words
    as fit within width, joined by one space. A word longer than width is
    cut into pieces of width characters, each on its own line, and the last
    piece starts the next line. Raises ValueError when width < 1."""
    if width < 1:
        raise ValueError("width < 1")
    lines = []
    cur = []
    cur_len = 0
    append_line = lines.append
    append_cur = cur.append
    for w in text.split(" "):
        if not w:
            continue
        lw = len(w)
        if lw > width:
            if cur:
                append_line(" ".join(cur))
                cur.clear()
                cur_len = 0
            while lw > width:
                append_line(w[:width])
                w = w[width:]
                lw -= width
        if cur_len:
            if cur_len + lw < width:
                append_cur(w)
                cur_len += lw + 1
            else:
                append_line(" ".join(cur))
                cur.clear()
                append_cur(w)
                cur_len = lw
        else:
            append_cur(w)
            cur_len = lw
    if cur:
        append_line(" ".join(cur))
    return lines
