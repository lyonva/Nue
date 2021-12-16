import pandas as pd
import os

file = 'fairsmote+hpt.csv'
path = os.path.join( 'fairness-2021', file )

df = pd.read_csv( path )


df = df[  ["DS", "PP", "PT", "Duration"] ]
for ds in df["DS"].unique():
    for pp in df["PP"].unique():
        for pt in df["PT"].unique():
            values = df[ df["DS"] == ds ][ df["PP"] == pp ][ df["PT"] == pt ]["Duration"]
            print(f"{ds:30s} {pp:10s} {pt:15s} {values.mean()}")

