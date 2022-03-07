from math import sqrt
import numpy as np
from gd import pareto_frontier
from itertools import chain
import sys

def diversity_comparison_indicator(list_of_fronts, lo, hi, divs = None):
    if divs is None:
        divs = recomended_divs( len(list_of_fronts[0][0]) )
    non_dominated = pareto_frontier(list(chain.from_iterable(list_of_fronts)))
    list_of_fronts = [map_to_grid(points, lo, hi, divs) for points in list_of_fronts]
    hyperboxes = unique_hyperboxes(map_to_grid(non_dominated, lo, hi, divs))
    
    contributions = []
    for h in hyperboxes:
        row = []
        for i, front in enumerate(list_of_fronts):
            row += [ contribution_degree(front, h) ]
        contributions += [row]
    S = len(hyperboxes)
    dci = [0 for i in range(len(list_of_fronts))]
    for j in range(len(list_of_fronts)):
        for i in range(S):
            dci[j] += contributions[i][j]
        dci[j] *= 1/S
    return dci

def recomended_divs(n):
    if n == 3: return 19
    if n == 4: return 11
    if n == 5: return 10
    if n == 6: return 8
    if n == 7: return 7
    if n == 8: return 6
    return 5


def contribution_degree(front, h):
    m = len(h)
    dist = distance_hyperbox_front(front, h)
    if dist >= sqrt(m+1): return 0
    return 1 - dist**2 / (m+1)

def distance_hyperbox_front(front, h):
    return min( [ grid_distance(h, coord) for coord in front ] )

def grid_distance(h1, h2):
    d = 0
    for h1k, h2k in zip(h1, h2):
        d += (h1k - h2k)**2
    return sqrt(d)

def unique_hyperboxes(coords):
    unique = []
    for coord in coords:
        if coord not in unique:
            unique += [[x for x in coord]]
    return unique

def map_to_grid(points, lo, hi, divs):
    _, lower, size = set_grid(lo, hi, divs)
    return [ map_point_to_grid( p, lower, size, divs ) for p in points ]

def set_grid( lo, hi, divs ):
    upper = hi
    lower = [ lo[j] + (hi[j] - lo[j])/(2*divs) for j in range(len(hi)) ]
    size = [ (upper[j] - lower[j])/divs + sys.float_info.epsilon for j in range(len(hi)) ]
    return upper, lower, size

def map_point_to_grid( point, lower, size, divs ):
    return [ max(0,min(divs-1,int( (point[j] - lower[j])/size[j] ))) for j in range(len(lower)) ]

if __name__ == "__main__":
    # Generate some artificial data
    n_p = 13
    d = [[0, 1], [0.05, 0.9], [0.1, 0.8], [0.2, 0.6]]
    list_of_fronts = []
    for lo, hi in d:
        inc = (hi - lo)/n_p
        front = []
        for i in range(n_p+1):
            v1 = hi - inc*i
            for j in range(i+1):
                v2 = lo + inc*j
                v3 = 1 - v1 - v2
                front += [ [v1, v2, v3] ]
        list_of_fronts += [front]
    print( diversity_comparison_indicator(list_of_fronts, [0,0,0], [1,1,1]) )
