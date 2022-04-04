from cmath import inf
from numpy import NaN
from math import sqrt

def generational_distance_plus(points, max_frontier, bounds):
    points = normalize(points, bounds)
    max_frontier = normalize(max_frontier, bounds)
    gd = 0
    p = len(points[0])
    n = len(points)
    for i in range(n):
        point = points[i]
        gd += min( [ gdp_euclidean_distance(point, r) for r in max_frontier ] )**p
    gd = (1/n) * gd**(1/p)
    return gd

def normalize_bounds(points):
    # Just returns bounds
    bounds = []
    for j in range(len(points[0])):
        lo, hi = inf, -inf
        for i in range(len(points)):
            lo = min(lo, points[i][j])
            hi = max(hi, points[i][j])
        bounds += [[lo, hi]]
    return bounds

def normalize(points, bounds = None):
    points = [ [x for x in p] for p in points ] # Copy just in case
    for j in range(len(points[0])):
        if bounds is None:
            lo, hi = inf, -inf
            for i in range(len(points)):
                lo = min(lo, points[i][j])
                hi = max(hi, points[i][j])
        else:
            lo, hi = bounds[j][0], bounds[j][1]
        for i in range(len(points)):
            if hi == lo:
                points[i][j] = 1
            else:
                points[i][j] = (points[i][j] - lo)/(hi - lo)
    return points

def gdp_euclidean_distance(ai, r):
    m = len(ai)
    if len(r) != m: return NaN
    d = 0
    for j in range(m):
        d += max(0, r[j] - ai[j])**2
    return sqrt(d)


def pareto_frontier(points):
    # Search for the pareto front
    # 1) No solution in the front is strictly better than any other
    # 2) Solutions that are strictly worse are removed
    front = []
    n = len(points)
    d = len(points[0])
    
    # We do this process for each explored hyper-parameter
    for i in range(n):
        point = points[i]
        included = True # We start assuming the current parameter can be included
        
        # Now, check for each of the pareto-front
        # Whether it is overshadowed by any other parameter
        for fp in front:
            overshadowed = True # Assume it is, until we find a case it isnt
            
            # Check for each metric
            for j in range(d):
                # Check if metric is overshadowed
                overshadowed = overshadowed and ( fp[j] >= point[j] )
                if not overshadowed: break # If we found it is not, stop searching
            
            # If the point is overshadowed by someone in the front, it is not included
            included = included and not(overshadowed)
            if not included: break # End if we already found it its not included
        
        # If the metric was not overshadowed by anyone, its a new point
        # Now, find out if the new point overshadows some of the existing points
        if included:            
            for fp in front:
                overshadowed = True # Assume it is, until we find a case it isnt
                
                # Check for each metric
                for j in range(d):
                    # Check if point is overshadowed
                    overshadowed = overshadowed and ( point[j] >= fp[j] )
                    if not overshadowed: break # If we found it is not, stop searching
                
                # If it is overshadowed by the new point, remove
                if overshadowed: front.remove(fp)
            
            # Lastly, add the new point to the front
            front.append(point)
    
    return front