def sort_people(people):
    """people is a list of (name, age). Return a new list, oldest first.
    People with the same age keep their order from the input."""
    out = []
    for p in people:
        i = len(out)
        while i > 0 and out[i - 1][1] < p[1]:
            i -= 1
        out.insert(i, p)
    return out
