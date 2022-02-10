import numpy as np

def distance_numeric_norm(df, col, i, j):
    c = df[col]
    low, high = c.min(), c.max()
    return abs(float(c[i]) - float(c[j])) / ( high - low )

def distance_str(df, col, i, j):
    

