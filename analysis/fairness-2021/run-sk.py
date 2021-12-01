from sk.sk import Rx, xtile
import os
import pandas as pd

def pos(lst, p): return sorted(lst)[int(len(lst)*p)]

df = ["ds", "pp", "pt", "m", "rank", "q0", "q1", "q2", "q3", "q4"]
df = dict( (x, []) for x in df )

dir = os.path.join("fairness-2021", "reshaped")
files = [ f for f in os.listdir( dir ) if os.path.isfile( os.path.join( dir, f ) ) ]

for f in files:
    path = os.path.join( dir, f )
    ds, m = f.split(".")[0].split("_", 1)
    res = Rx.fileIn(path)
    max_rank = max([ rx.rank for rx in res ])
    for rx in res:
        pp, pt = rx.rx.split("+",1)
        vals = rx.vals
        gib = m in ["accuracy", "precision", "recall", "f1"]
        rank = rx.rank
        if gib:
            rank = 1 + max_rank - rx.rank
        
        df["ds"] += [ds]
        df["pp"] += [pp]
        df["pt"] += [pt]
        df["m"] += [m]
        df["rank"] += [rank]
        df["q0"] += [min(vals)]
        df["q1"] += [pos(vals, 0.25)]
        df["q2"] += [pos(vals, 0.5)]
        df["q3"] += [pos(vals, 0.75)]
        df["q4"] += [max(vals)]

df = pd.DataFrame.from_dict(df)
df.to_csv( os.path.join("fairness-2021", "sk-res.csv"), index = False )

df_simple = pd.read_csv( os.path.join("fairness-2021", "simple-res.csv") )
df_simple = df_simple.melt(id_vars=["DS","PP","PT"])
df_join = df[ ["ds", "pp", "pt", "m", "rank"] ]
df_simple.columns = [ "ds", "pp", "pt", "m", "val" ]
df_s_rank = df_simple.set_index( ["ds", "pp", "pt", "m"] ).join(df_join.set_index( ["ds", "pp", "pt", "m"] ), how='left')
df_s_rank = df_s_rank.reset_index()
df_s_rank.to_csv( os.path.join("fairness-2021", "simple-rank-res.csv"), index = False )
