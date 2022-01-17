import pandas as pd
import os

df = pd.read_csv( os.path.join( "fairness-2021", "sk-res.csv" ) )
ds_list = df["ds"].unique()
df["tech"] = df["pp"] + "+" + df["pt"]
df = df[ ["ds", "tech", "m", "rank"] ]

for ds in ds_list:
    sub = df[ df["ds"] == ds ]
    sub = sub[ ["tech", "m", "rank"] ]
    piv = sub.pivot( index = "tech", columns = "m", values = "rank" )
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(ds)
        print(piv)
        print()
