import pandas as pd
import os

df = pd.read_csv(os.path.join( 'combo-three', "sk-res.csv" ))
df["iqr"] = df["q3"] - df["q1"]

files = ["china", "desharnais", "isbsg10", "osp", "osp2", "ground", "flight"]
for file in files:
    path = os.path.join( 'combo-three', "result-" + file + ".csv" )
    df_simple = pd.read_csv( path )
    df_simple = df_simple.drop(["Iteration"], axis=1)
    df_simple["PT"] = ['random' if x == "random search" else x for x in df_simple["PT"]]
    df_simple = df_simple.set_index( "PT" )
    mean = df_simple.mean( level=0 )
    std = df_simple.std(level = 0)
    mean = mean.reset_index()
    std = std.reset_index()
    mean = mean.melt(id_vars=["PT"])
    std = std.melt(id_vars=["PT"])
    mean.columns = ["pt", "m", "mean"]
    std.columns = ["pt", "m", "std"]
    mean_std = mean.set_index( ["pt", "m"] ).join(std.set_index( ["pt", "m"] ), how='left')
    mean_std = mean_std.reset_index()
    df_join = df[ df["ds"] == file ][ ["pt", "m", "rank", "q2", "iqr"] ]
    df_join.columns = ["pt", "m", "rank", "median", "iqr"]
    df_s_rank = mean_std.set_index( ["pt", "m"] ).join(df_join.set_index( ["pt", "m"] ), how='left')
    df_s_rank = df_s_rank.reset_index()
    df_s_rank.to_csv( os.path.join("combo-three", "result-" + file + "-summary+rank.csv"), index = False )