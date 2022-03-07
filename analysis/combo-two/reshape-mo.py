import pandas as pd
import os

files = ["china", "isbsg10", "osp", "osp2", "ground", "flight"]
for file in files:
    path = os.path.join( 'combo-two', "mo-" + file + ".csv" )

    df = pd.read_csv( path )
    
    m_list = df.columns[2:]
    pt_list = df["PT"].unique()

    for m in m_list:
        res = {}
        
        for pt in pt_list:
            values = df[ df["PT"] == pt ][m]
            values = list(values.dropna())
            treatment = f'{pt if pt != "random search" else "random"}'
            if len(values) > 0:
                res[treatment] = values
        m = m.split(" ")[0]
        # to_file = ds.split("/")[1].split(".")[0].split("_")[0] + "_" + m + ".csv"
        to_file = file + "_" + m + ".csv"
        to_file = path = os.path.join( 'combo-two', 'reshaped', to_file )
        if len(res) > 0:
            new_df = pd.DataFrame.from_dict( res, orient='index' )
            new_df.to_csv( to_file, header = None, sep = " " )
        

