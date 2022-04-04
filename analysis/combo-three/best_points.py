from math import exp
import pandas as pd
from gd import normalize
from headers import *

def pareto_frontier_zitler(points):
    # Search for the pareto front
    # 1) No solution in the front is strictly better than any other
    # 2) Solutions that are strictly worse are removed
    front = []
    n = len(points)
    d = len(points[0])

    points = normalize(points)
    
    # We do this process for each explored hyper-parameter
    for i in range(n):
        point = points[i]
        included = True # We start assuming the current parameter can be included
        
        # Now, check for each of the pareto-front
        # Whether it is overshadowed by any other parameter
        for fp in front:
            fpp = points[fp]
            overshadowed = zitler_dominates( fpp, point ) == 1
            
            # If the point is overshadowed by someone in the front, it is not included
            included = included and not(overshadowed)
            if not included: break # End if we already found it its not included
        
        # If the metric was not overshadowed by anyone, its a new point
        # Now, find out if the new point overshadows some of the existing points
        if included:            
            for fp in front:
                fpp = points[fp]
                overshadowed = zitler_dominates( point, fpp ) == 1
                
                # If it is overshadowed by the new point, remove
                if overshadowed: front.remove(fp)
            
            # Lastly, add the new point to the front
            front.append(i)
    
    return front

def zitler_dominates(a, b):
    """Returns wether a zitler dominates b
    Requires a and b to be normalized in [0, 1] range
    1: a dominates b
    -1: a is dominated by b
    0: Neither dominates, equivalent"""
    s1, s2 = 0, 0
    n = len(a)
    for ai, bi in zip(a, b):
        s1 -= exp( (ai - bi)/n )
        s2 -= exp( (bi - ai)/n )
    if s1/n < s2/n:
        return 1
    elif s1/n > s2/n:
        return -1
    else:
        return 0

dir = "combo-three"
dss = ["osp", "osp2", "ground", "flight"]

for ds in dss:
    path = dir + "/" + "result-hpt-" + ds + ".csv"
    df = pd.read_csv(path)

    x = get_x(df)
    headers = df[x].drop_duplicates()
    x.remove("Iteration")
    y = get_y(df)
    df = mult_by_sign(df)
    
    x_u = df[x].drop_duplicates()
    i_u = df["Iteration"].max() + 1

    all = pd.DataFrame()

    for i in range(i_u):
        
        for _, u in x_u.iterrows():
            frontier = df[ df["Iteration"] == i ]
            for xv in x:
                frontier = frontier[ frontier[xv] == u[xv] ]
            frontier_p = frontier[y].values.tolist()
            best_idx = pareto_frontier_zitler( frontier_p )
            best = frontier.iloc[ best_idx,: ]
            
            all = pd.concat([all, best], axis = 0)
    
    all = mult_by_sign(all)
    all = all.drop(["Parameters?"], axis=1)
    all.to_csv( dir + "/" + "result-" + ds + ".csv", index = False )
