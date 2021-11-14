import pandas as pd
import numpy as np
import random

seed = 113094
files = ["Scrum1k.csv", "Scrum10k.csv", "Scrum100.csv", "Scrum100k.csv",
         "billing10k.csv", "FFM-125-25-0.50-SAT-1.csv", "FFM-250-50-0.50-SAT-1.csv",
         "FFM-500-100-0.50-SAT-1.csv", "FFM-1000-200-0.50-SAT-1.csv",
         "FM-500-100-0.25-SAT-1.csv", "FM-500-100-0.50-SAT-1.csv",
         "FM-500-100-0.75-SAT-1.csv", "FM-500-100-1.00-SAT-1.csv"]
prob_one = 0.5


for filename in files:
    random.seed(seed)
    
    # Load set and create artificial column names
    df = pd.read_csv( filename, header=None )
    n_col = df.shape[1]
    n_row = df.shape[0]
    colnames = [ f'feature {i+1:03d}' for i in range(n_col) ]
    df.columns = colnames
    print(df)
    
    # Oracle
    new_column = [ 1 if random.random() < prob_one else 0 for i in range(n_row) ]
    df["Target"] = new_column
    
    name, ext = ".".join(filename.split(".")[:-1]), filename.split(".")[-1]
    df.to_csv( f"{name}-{seed}.{ext}", index = False )