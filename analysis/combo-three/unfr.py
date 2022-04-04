def unique_nondominated_front_ratio(frontier, max_frontier):
    r = 0
    for f in frontier:
        count = True
        for mf in max_frontier:
            if strong_dominates(mf, f):
                count = False
                break
        if count:
            r += 1
    return r / len(max_frontier)

def weak_dominates(a, b):
    d = len(a)
    for i in range(d):
        if a[i] < b[i]:
            return False
    return True

def strong_dominates(a, b):
    if not(weak_dominates(a, b)):
        return False
    d = len(a)
    for i in range(d):
        if a[i] > b[i]:
            return True
    return False

