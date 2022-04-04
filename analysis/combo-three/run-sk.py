import os
from sk.sk import Rx, xtile
import pandas as pd

def pos(lst, p): return sorted(lst)[int(len(lst)*p)]

df = ["ds", "pt", "m", "rank", "q0", "q1", "q2", "q3", "q4"]
df = dict( (x, []) for x in df )

dir = os.path.join("combo-three", "reshaped")
files = [ f for f in os.listdir( dir ) if os.path.isfile( os.path.join( dir, f ) ) ]

for f in files:
    path = os.path.join( dir, f )
    ds, m = f.split(".")[0].split("_", 1)
    res = Rx.fileIn(path)
    max_rank = max([ rx.rank for rx in res ])
    for rx in res:
        pt = rx.rx
        vals = rx.vals
        gib = m[-1] == "+"
        rank = rx.rank
        if gib:
            rank = 1 + max_rank - rx.rank
        
        df["ds"] += [ds]
        df["pt"] += [pt]
        df["m"] += [m]
        df["rank"] += [rank]
        df["q0"] += [min(vals)]
        df["q1"] += [pos(vals, 0.25)]
        df["q2"] += [pos(vals, 0.5)]
        df["q3"] += [pos(vals, 0.75)]
        df["q4"] += [max(vals)]

df = pd.DataFrame.from_dict(df)
df.to_csv( os.path.join("combo-three", "sk-res.csv"), index = False )


