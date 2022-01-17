import pandas as pd
import os

files = ['result-see', 'result-fairness']
for file in files:
    path = os.path.join( 'combo', file + ".csv" )

    df = pd.read_csv( path )


    df = df[ df.columns.difference( ["Iteration", "PP", "DT", "AS", "LA",
                                    "PT scoring", "Duration", "Models built",
                                    "Best params", "Params"] ) ] # Drop no use columns

    df["DS"] = [ x.split("/")[1].split(".")[0].split("_")[0] for x in df["DS"] ]
    df.columns = [ x.split(" ")[0] for x in df.columns ]
    df["PT"] = [ "random" if x == "random search" else x for x in df["PT"] ]
    # df["tech"] = [ x + "+" + y for x, y in zip( df["PP"], df["PT"] )  ]


    df.to_csv( os.path.join( 'combo', file + "-simple.csv" ), index = None )
        

