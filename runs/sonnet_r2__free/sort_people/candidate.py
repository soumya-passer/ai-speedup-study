from operator import itemgetter


def sort_people(people):
    """people is a list of (name, age). Return a new list, oldest first.
    People with the same age keep their order from the input."""
    return sorted(people, key=itemgetter(1), reverse=True)
