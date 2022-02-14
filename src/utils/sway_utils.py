import numpy as np

def distance_numeric_norm(df, col, i, j):
    c = df[col]
    low, high = min(c), max(c)
    return abs(float(c[i]) - float(c[j])) / ( high - low )

def distance_str(df, col, i, j):
    return 0 if df[col][i] == df[col][j] else 1

def distance_pair(df, types, i, j, p = 2):
    """
        Calculate distance between items i and j
        p is power, p = 2 is euclidean, etc
    """
    d = 0
    for t, v in types.items():
        f = distance_str
        if v in ["f", "i"]:
            f = distance_numeric_norm
        d += pow(f( df, t, i, j ), p)
    d /= len(types)
    d = pow(d, 1/p)
    return d

def distance_from(df, types, idx, i, p = 2):
    return [ distance_pair(df, types, i, j, p = p) for j in idx ]
