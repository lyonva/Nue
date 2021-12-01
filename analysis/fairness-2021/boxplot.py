import pandas as pd
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt

df = pd.read_csv( os.path.join( "fairness-2021", "simple-rank-res.csv" ) )
df["pp"] = [ "fs" if x == 'fairsmote' else x for x in df["pp"] ]
df["pt"] = [ "rs" if x == 'random' else x for x in df["pt"] ]
df["tech"] = [ x + "+rf+" + y for x, y in zip( df["pp"], df["pt"] ) ]
df["tech"] = [ x.replace("none+","").upper() for x in df["tech"] ]
df["tech"] = [ x.replace("+DEFAULT","").upper() for x in df["tech"] ]
df = df[ [x in ["d2h1", "d2h2", "d2h3"] for x in df["m"]] ]
df["d2h"] = [ "overall" if x == "d2h1" else "classification" if x == "d2h2" else "fairness" for x in df["m"] ]

ds_list = df["ds"].unique()
m_list = ["d2h1", "d2h2", "d2h3"]
mn_list = ["Prediction", "Fairness", "Overall"]
tech_list = df["tech"].unique()

for ds in ds_list:
    
    top, bottom = [], []
    for m in m_list:
        
        for t in tech_list:
            sub_df = df[ np.logical_and(np.logical_and(df["ds"]==ds, df["m"]==m), df["tech"]==t) ]
            val = sub_df["val"]
            iqr = val.quantile(0.75) - val.quantile(0.25)
            bottom += [val.quantile(0.25) - 1.5*iqr]
            top += [val.quantile(0.75) + 1.5*iqr]
    top, bottom = max(top), min(bottom)
    
    
    for m, mn in zip( m_list, mn_list ):
        
        sub_df = df[ np.logical_and(df["ds"]==ds, df["m"]==m) ]
        
        ranks = pd.DataFrame([ sub_df[ sub_df["tech"] == x ].iloc[0][["tech", "rank"]] for x in tech_list ])
        ranks = ranks.sort_values(by=['rank'])
        
        plt.clf()
        fig, ax = plt.subplots(figsize=(5, 8.5))
        plt.ylim((bottom, top))
        plt.tight_layout(pad=2.25)
        ax.tick_params(axis='x', rotation=25)
        g = sns.boxplot( x = "tech", y = "val", hue = "rank",
                    data = sub_df, dodge = False, order = list(ranks["tech"]),
                    showfliers = False, 
                    palette = sns.cubehelix_palette(start=1.5, rot=0.4,
                                                    dark=0.35, light=1, reverse=True)
            ).set(
                xlabel='Model', 
                ylabel='Distance to heaven',
                title=f'{mn}',
            )
        ax.get_legend().remove()
        fig.savefig( os.path.join( "fairness-2021", "box", f"box-{ds}-{m}.png" ) )
        plt.close()
        
