def word_wrap(text, width):
    """Greedy wrap. Words are separated only by the space character; tabs,
    new lines and hyphens are part of a word. Each line holds as many words
    as fit within width, joined by one space. A word longer than width is
    cut into pieces of width characters, each on its own line, and the last
    piece starts the next line. Raises ValueError when width < 1."""
    if width < 1:
        raise ValueError("width < 1")

    # Fast path: text is single-spaced (no leading/trailing or double
    # spaces). Then every output line is a contiguous slice of the input,
    # so we can locate line breaks with C-level rfind/slicing instead of
    # splitting and re-joining every word in Python.
    if text and text[0] != " " and text[-1] != " " and "  " not in text:
        lines = []
        append = lines.append
        rfind = text.rfind
        n = len(text)
        pos = 0
        while pos < n:
            if pos + width >= n:
                append(text[pos:])
                break
            # Last space at index <= pos + width gives the longest line
            # that fits; if there is none, the first word exceeds width
            # and must be cut into a width-sized chunk.
            idx = rfind(" ", pos + 1, pos + width + 1)
            if idx < 0:
                append(text[pos:pos + width])
                pos += width
            else:
                append(text[pos:idx])
                pos = idx + 1
        return lines

    # General path: arbitrary spacing. Track current line length instead
    # of re-joining all words in it on every step.
    words = list(filter(None, text.split(" ")))
    lines = []
    append = lines.append
    cur = []
    cur_len = 0
    for w in words:
        lw = len(w)
        if lw > width:
            if cur:
                append(" ".join(cur))
                cur = []
                cur_len = 0
            # Full width-sized chunks are lines on their own; the
            # remainder (1..width chars) starts the next line.
            chunk_end = ((lw - 1) // width) * width
            start = 0
            while start < chunk_end:
                append(w[start:start + width])
                start += width
            cur = [w[chunk_end:]]
            cur_len = lw - chunk_end
        elif cur:
            if cur_len + 1 + lw <= width:
                cur.append(w)
                cur_len += 1 + lw
            else:
                append(" ".join(cur))
                cur = [w]
                cur_len = lw
        else:
            cur = [w]
            cur_len = lw
    if cur:
        append(" ".join(cur))
    return lines
