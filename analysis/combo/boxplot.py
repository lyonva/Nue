import pandas as pd
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt

df = pd.read_csv( os.path.join( "combo", "result-fairness-simple-rank.csv" ) )
df["pt"] = [ "rs" if x == 'random' else x for x in df["pt"] ]
df = df[ [x in ["d2h1", "d2h2", "d2h3", "accuracy", "precision", "recall", "f1"] for x in df["m"]] ]

ds_list = df["ds"].unique()
m_list = ["d2h1", "d2h2", "d2h3", "accuracy", "precision", "recall", "f1"]
mn_list = ["d2h Prediction", "d2h Fairness", "d2h Overall", "accuracy", "precision", "recall", "f1"]
tech_list = df["pt"].unique()

for ds in ds_list:
    
    top, bottom = [], []
    for m in m_list:
        
        for t in tech_list:
            sub_df = df[ np.logical_and(np.logical_and(df["ds"]==ds, df["m"]==m), df["pt"]==t) ]
            val = sub_df["val"]
            iqr = val.quantile(0.75) - val.quantile(0.25)
            bottom += [val.quantile(0.25) - 1.5*iqr]
            top += [val.quantile(0.75) + 1.5*iqr]
    top, bottom = max(top), min(bottom)
    
    
    for m, mn in zip( m_list, mn_list ):
        
        sub_df = df[ np.logical_and(df["ds"]==ds, df["m"]==m) ]
        
        ranks = pd.DataFrame([ sub_df[ sub_df["pt"] == x ].iloc[0][["pt", "rank"]] for x in tech_list ])
        ranks = ranks.sort_values(by=['rank'])
        
        plt.clf()
        fig, ax = plt.subplots(figsize=(8, 10))
        plt.ylim((bottom, top))
        plt.tight_layout(pad=2.25)
        ax.tick_params(axis='x', rotation=25)
        g = sns.boxplot( x = "pt", y = "val", hue = "rank",
                    data = sub_df, dodge = False, order = list(ranks["pt"]),
                    showfliers = False, 
                    palette = sns.cubehelix_palette(start=1.5, rot=0.4,
                                                    dark=0.35, light=1, reverse=True)
            ).set(
                xlabel='Model', 
                ylabel='Distance to heaven',
                title=f'{ds} - {mn}',
            )
        ax.get_legend().remove()
        fig.savefig( os.path.join( "combo", "box", f"box-{ds}-{m}.png" ) )
        plt.close()
        

# SEE
df = pd.read_csv( os.path.join( "combo", "result-see-simple-rank.csv" ) )
df["pt"] = [ "rs" if x == 'random' else x for x in df["pt"] ]
df = df[ [x in ["sa", "sd", "mar", "sdar"] for x in df["m"]] ]

ds_list = df["ds"].unique()
m_list = ["sa", "sd", "mar", "sdar"]
mn_list = ["SA", "SD", "MAR", "SDAR"]
tech_list = df["pt"].unique()

for ds in ds_list:
    
    
    
    
    for m, mn in zip( m_list, mn_list ):
        top, bottom = [], []
        for t in tech_list:
            sub_df = df[ np.logical_and(np.logical_and(df["ds"]==ds, df["m"]==m), df["pt"]==t) ]
            val = sub_df["val"]
            iqr = val.quantile(0.75) - val.quantile(0.25)
            bottom += [val.quantile(0.25) - 1.5*iqr]
            top += [val.quantile(0.75) + 1.5*iqr]
        top, bottom = max(top), min(bottom)
        
        sub_df = df[ np.logical_and(df["ds"]==ds, df["m"]==m) ]
        
        ranks = pd.DataFrame([ sub_df[ sub_df["pt"] == x ].iloc[0][["pt", "rank"]] for x in tech_list ])
        ranks = ranks.sort_values(by=['rank'])
        
        plt.clf()
        fig, ax = plt.subplots(figsize=(8, 10))
        plt.ylim((bottom, top))
        plt.tight_layout(pad=2.25)
        ax.tick_params(axis='x', rotation=25)
        g = sns.boxplot( x = "pt", y = "val", hue = "rank",
                    data = sub_df, dodge = False, order = list(ranks["pt"]),
                    showfliers = False, 
                    palette = sns.cubehelix_palette(start=1.5, rot=0.4,
                                                    dark=0.35, light=1, reverse=True)
            ).set(
                xlabel='Model', 
                ylabel=f'{m}',
                title=f'{ds} - {mn}',
            )
        ax.get_legend().remove()
        fig.savefig( os.path.join( "combo", "box", f"box-{ds}-{m}.png" ) )
        plt.close()
        
