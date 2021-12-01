import pandas as pd
import os

file = 'fairsmote+hpt.csv'
path = os.path.join( 'fairness-2021', file )

df = pd.read_csv( path )


df = df[ df.columns.difference( ["Iteration", "DT", "AS", "LA",
                                "PT scoring", "Duration", "Models built",
                                "Best params"] ) ] # Drop no use columns
print(df.columns)
ds_list = df["DS"].unique()
m_list = df.columns[3:]
pp_list = df["PP"].unique()
pt_list = df["PT"].unique()

for ds in ds_list:
    for m in m_list:
        res = {}
        
        for pp in pp_list:
            for pt in pt_list:
                values = df[ df["DS"] == ds ][ df["PP"] == pp ][ df["PT"] == pt ][m]
                values = list(values.dropna())
                treatment = f'{pp}+{pt if pt != "random search" else "random"}'
                if len(values) > 0:
                    res[treatment] = values
        m = m.split(" ")[0]
        to_file = ds.split("/")[1].split(".")[0].split("_")[0] + "_" + m + ".csv"
        to_file = path = os.path.join( 'fairness-2021', 'reshaped', to_file )
        if len(res) > 0:
            new_df = pd.DataFrame.from_dict( res, orient='index' )
            new_df.to_csv( to_file, header = None, sep = " " )
        

