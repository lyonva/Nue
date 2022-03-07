import pandas as pd

from headers import *
from hv import *
from gd import *
from dci import *
from unfr import *

dir = "two"
dss = ["china", "isbsg10", "osp", "osp2", "ground", "flight"]

for ds in dss:
    path = "../results/" + dir + "/" + "result-" + ds + "-pareto.csv"
    df = pd.read_csv(path)

    x = get_x(df)
    headers = df[x].drop_duplicates()
    x.remove("Iteration")
    y = get_y(df)
    df = mult_by_sign(df)
    # Remove dull solutions, ie negative and 0 points
    if ds in ["china", "isbsg10"]:
        df = df[(df[y] > 0).all(1)]

    # all_y = df[y].values.tolist()
    # max_frontier = pareto_frontier( all_y )
    # bounds = normalize_bounds( all_y )
    # ideal = best( all_y )
    # nadir = worst( all_y )

    x_u = df[x].drop_duplicates()
    i_u = df["Iteration"].max() + 1
    hv = []
    gd = []
    dci = []
    unfr = []

    for i in range(i_u):
        iter_fronts = []
        iter_y = df[ df["Iteration"] == i ][y].values.tolist()
        if( len(iter_y) == 0 ):
            hv += [ 0 for i in range(x_u.shape[0]) ]
            gd += [ 1 for i in range(x_u.shape[0]) ]
            dci += [ 0 for i in range(x_u.shape[0]) ]
            unfr += [ 0 for i in range(x_u.shape[0]) ]
            continue
        max_frontier = pareto_frontier( iter_y )
        bounds = normalize_bounds( iter_y )
        ideal = best( iter_y )
        nadir = worst( iter_y )
        
        for _, u in x_u.iterrows():
            frontier = df[ df["Iteration"] == i ]
            for xv in x:
                frontier = frontier[ frontier[xv] == u[xv] ]
            frontier = frontier[y].values.tolist()
            if len(frontier) == 0:
                frontier = [nadir]
            
            iter_fronts += [frontier]
            hv += [ hyper_volume(frontier, nadir) ]
            gd += [ generational_distance_plus(frontier, max_frontier, bounds) ]
            unfr += [ unique_nondominated_front_ratio(frontier, iter_y) ]
        dci += diversity_comparison_indicator(iter_fronts, nadir, ideal )
        

    headers["HV+"] = hv
    headers["GD-"] = gd
    headers["DCI+"] = dci
    headers["UNFR+"] = unfr

    headers.to_csv("combo-two/mo-"+ds+".csv", index=False)

    

