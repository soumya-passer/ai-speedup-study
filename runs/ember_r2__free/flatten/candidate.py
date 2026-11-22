def flatten(x):
    """x is a list. Lists and tuples inside it, at any depth (even 5,000
    levels), are opened up. Everything else - numbers, strings, bytes,
    dicts - is kept as one item. Returns a new flat list, in order."""
    out = []
    out_append = out.append
    out_extend = out.extend
    stack = []

    def expand_large(lst):
        # lst is a list/tuple with many elements. Find runs of
        # non-containers using C-level map/type and list.index
        # (instead of a Python-level scan), and push frames for each
        # run (a flat slice, extended in C) and each container, in
        # reverse order so they are popped in original order.
        types = list(map(type, lst))
        n = len(types)
        pos = 0
        segments = []
        seg_append = segments.append
        while pos < n:
            try:
                i_list = types.index(list, pos)
            except ValueError:
                i_list = n
            try:
                i_tuple = types.index(tuple, pos, i_list)
            except ValueError:
                i_tuple = n
            p = i_list if i_list < i_tuple else i_tuple
            if p >= n:
                if pos < n:
                    seg_append((False, lst[pos:n]))
                break
            if p > pos:
                seg_append((False, lst[pos:p]))
            seg_append((True, lst[p]))
            pos = p + 1
        for is_container, item in reversed(segments):
            if is_container:
                if len(item) > 48:
                    stack.append({0: item})
                else:
                    stack.append(iter(item))
            else:
                stack.append(item)

    if (type(x) is list or type(x) is tuple) and len(x) > 48:
        expand_large(x)
    else:
        stack.append(iter(x))

    while stack:
        frame = stack[-1]
        ft = type(frame)
        if ft is list or ft is tuple:
            out_extend(frame)
            stack.pop()
            continue
        if ft is dict:
            stack.pop()
            expand_large(frame[0])
            continue
        for v in frame:
            t = type(v)
            if t is list or t is tuple:
                if len(v) > 48:
                    stack.append({0: v})
                else:
                    stack.append(iter(v))
                break
            out_append(v)
        else:
            stack.pop()
    return out
