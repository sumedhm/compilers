def has_duplicates(d):
    return len(d) != len(set(d.values()))

print has_duplicates({'a': 1, 'b': 3, 'c': 2})