# QHV-II
# Reference: Improved Quick Hypervolume Algorithm, Andrzej Jaszkiewicz

def hyper_volume(pts, ref):
    hi = best(pts)
    return quick_hyper_volume_ii(pts, ref, hi)

def quick_hyper_volume_ii(p, lo, hi):
    if len(p) == 0: return 0
    if len(p) == 1: return hv_2_points( lo, p[0] )
    if len(p) == 2: return hv_2_points( lo, p[0] ) + hv_2_points( lo, p[1] ) - hv_2_points( lo, worst(p) )
    n = len(p)
    # Select pivot
    hv = 0
    pv = -1
    for i in range(n):
        n_hv = hv_2_points(lo, p[i])
        if n_hv > hv:
            hv = n_hv
            pv = i
    # Sanity check, we may have all points not dominating lo
    if hv == 0:
        return 0
    # Parition space into d hypercubes
    parts = partition(p[pv], lo, hi)[:-1]
    for (part_lo, part_hi) in parts:
        new_p = []
        for i in range(n):
            if in_range(p[i], part_lo, part_hi):
                new_p += [p[i]]
        hv += quick_hyper_volume_ii( new_p, part_lo, part_hi )
    return hv

def in_range(p, lo, hi):
    d = len(p)
    for i in range(d):
        if not(lo[i] < p[i] <= hi[i]):
            return False
    return True

def hv_2_points(lo, hi):
    v = 1
    d = len(lo)
    for i in range(d):
        if(hi[i] <= lo[i]):
            return 0
        v *= (hi[i] - lo[i])
    return v

def decypher_point(p, lo, me, hi):
    n_p = []
    for i, pi in enumerate(p):
        if pi == "h":
            n_p += [ hi[i] ]
        if pi == "m":
            n_p += [ me[i] ]
        if pi == "l":
            n_p += [ lo[i] ]
    return n_p

def worst(pts):
    d = len(pts[0])
    n = len(pts)
    x = [ pts[0][i] for i in range(d) ]
    for i in range(n):
        for j in range(d):
            x[j] = min(x[j], pts[i][j])
    return x

def best(pts):
    d = len(pts[0])
    n = len(pts)
    x = [ pts[0][i] for i in range(d) ]
    for i in range(n):
        for j in range(d):
            x[j] = max(x[j], pts[i][j])
    return x

def partition(p, lo, hi):
    # Returns last partition (space between low and p)
    # But it should be commonly ignored
    res = []
    d = len(lo)
    for i in range(d+1):
        n_lo = "l" * i + "m" + "l" * (d-i-1)
        n_lo = n_lo[0:d]
        n_hi = "m" * i + "h" * (d-i)

        res += [[decypher_point(n_lo, lo, p, hi), decypher_point(n_hi, lo, p, hi)]]
    return res

if __name__ == "__main__":
    e = partition([2,2,2], [1,1,1], [3,3,3])
    print(e)
    for lo, hi in e:
        print( hv_2_points(lo, hi) )
    print( hv_2_points([1,1,1], [3,3,3]) )

    print( worst([[1,2,3,3], [3,2,1,1]]) )

    print( best([[1,2,3,3], [3,2,1,1]]) )

    e = partition([2,2,2], [1,1,1], [3,3,3])[:-1]
    print(e)

    print( hyper_volume([[2,2], [2.5,1.5], [1.5,2.5]], [0,0]) ) # Should be 5.
    print( hyper_volume([[2,2], [2.5,1.5], [1.5,2.5], [1,1], [2, 1.5], [1.5, 2], [1.4, 2.4], [2.4, 1.4]], [0,0]) ) # Should be 5.5
    print( hyper_volume([[2,2], [2.5,1.5], [1.5,2.5]], [1,1]) ) # Should be 1.5