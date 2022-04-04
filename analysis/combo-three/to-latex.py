import pandas as pd
import os
import numpy as np

line_end = " \\\\\n"

files = ["china", "desharnais", "isbsg10", "osp", "osp2", "ground", "flight"]
percentage_metrics = ["SA+", "SD+", "MMRE-", "MdMRE-", "Pred25+", "Pred40+", "Delta+"]
to_show = ["MAR-", "SA+", "MdMRE-", "Pred40+", "Effort-" ,"Months-","Defects-", "Risks-"]
opt_map = {'nsga-iii' : "NSGA-III", 'random' : "Random64", 'sway' : "SWAY", 'moead' : "MOEA/D", 'tpe' : "TPE", 'nsga-ii' : "NSGA-II", 'default' : "Default",
    "Random1024" : "Random1024", "Random300" : "Random300", "random300" : "Random300", "random150" : "random150", "random60" : "random60"}
for file in files:
    path = os.path.join( 'combo-three', "result-" + file + "-summary+rank.csv" )

    df = pd.read_csv( path )
    df = df[[x in to_show for x in df["m"]]]
    print(df)
    mean = df.pivot( index="pt", columns="m", values="mean" )
    mean = mean.drop( [x for x in mean.columns if x[-1] == "?"], axis = 1 ).reset_index()
    median = df.pivot( index="pt", columns="m", values="median" )
    median = median.drop( [x for x in median.columns if x[-1] == "?"], axis = 1 ).reset_index()
    std = df.pivot( index="pt", columns="m", values="std" )
    std = std.drop( [x for x in std.columns if x[-1] == "?"], axis = 1 ).reset_index()
    iqr = df.pivot( index="pt", columns="m", values="iqr" )
    iqr = iqr.drop( [x for x in iqr.columns if x[-1] == "?"], axis = 1 ).reset_index()
    rank = df.pivot( index="pt", columns="m", values="rank" ).reset_index()
    rank = rank.drop( [x for x in rank.columns if x[-1] == "?"], axis = 1 )

    metrics = [c for c in mean.columns if c[-1] in ["+", "-"] and c in to_show]
    optimizers = list( mean["pt"].unique() )
    wins = dict( (k, df[df["pt"] == k][df["rank"] == 1]["rank"].sum() ) for k in optimizers )
    optimizers = sorted( optimizers, key = lambda x : wins[x], reverse=True )
    
    s = ""
    s += "\\begin{table*}[t]" + "\n"
    s += "\\caption{Results for the " + file + " model. Cells read as `mean [median iqr]'.}" + "\n"
    s += "\\label{tab-res-"+ file +"}"  + "\n"
    s += "\\begin{tabular}{@{}lr" + "r"*len(metrics) + "@{}}" + "\n"

    s += "\\toprule" + "\n"
    s += " & ".join(["Search", "Wins"] + metrics) + line_end
    
    last_win = -1

    for o in optimizers:

        win = wins[o]
        if last_win != win:
            s += "\\midrule" + "\n"
        last_win = win
        
        row = [opt_map[o], f"{win:.0f}"]

        for m in metrics:
            me = mean[mean["pt"] == o][m].values[0]
            md = median[median["pt"] == o][m].values[0]
            iq = iqr[iqr["pt"] == o][m].values[0]
            if m in percentage_metrics:
                me *= 100
                md *= 100
                iq *= 100
            w = rank[rank["pt"] == o][m].values[0]
            x = "\\cellcolor[HTML]{C0C0C0}" if w == 1 else ""
            row += [ x + f"{me:.1f} [{md:.1f} {iq:.1f}]" ]
        
        s +=  " & ".join( row ) + line_end
    
    s += "\\bottomrule" + "\n"
    s += "\\end{tabular}" + "\n"
    s += "\\end{table*}" + "\n"
        
    with open(os.path.join("combo-three", "latex-tab-"+file+".txt"), "w") as out:
        out.write(s)
