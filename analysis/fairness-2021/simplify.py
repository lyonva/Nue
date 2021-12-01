import pandas as pd
import os

file = 'fairsmote+hpt.csv'
path = os.path.join( 'fairness-2021', file )

df = pd.read_csv( path )


df = df[ df.columns.difference( ["Iteration", "DT", "AS", "LA",
                                "PT scoring", "Duration", "Models built",
                                "Best params"] ) ] # Drop no use columns

df["DS"] = [ x.split("/")[1].split(".")[0].split("_")[0] for x in df["DS"] ]
df.columns = [ x.split(" ")[0] for x in df.columns ]
df["PT"] = [ "random" if x == "random search" else x for x in df["PT"] ]
# df["tech"] = [ x + "+" + y for x, y in zip( df["PP"], df["PT"] )  ]


df.to_csv( os.path.join( 'fairness-2021', "simple-res.csv" ), index = None )
        

