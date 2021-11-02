# Libraries
import numpy as np
import pandas as pd

# TODO fix imports
from database.dataset_db import dataset_db
from database.cv_db import cv_db
from comp.Loader import Loader
from sklearn.model_selection import KFold

# Prelude
idx_dir = "idx/"
groups = 1 # Partition the indexes into different datasets? For multiple PCs

# Load configuration
FW, DS, DT, AS, PT, LA, EM = Loader().load_config()
datasets = dataset_db.get(DS)

# Cross Validation
# Defaults to 80:20 train test split
cv = cv_db[ FW["cv"][0] if "cv" in FW.keys() else "traintestsplit" ]( **(FW["cv"][1] if "cv" in FW.keys() else {"n_splits":1, "test_size":0.2}) )

# Dataset Loop
for ds in datasets:
    ds.set_datapath("data/")
    dataframe = ds.get_dataframe()
    
    # Data pre-processing
    # dataframe = prep.process(dataframe)
    X = dataframe[ dataframe.columns.difference([ds.predict]) ]
    Y = dataframe[ ds.predict ]
    
    train_set = []
    test_set = []
    
    # Cross validation
    for iteration, (train_index, test_index) in enumerate(cv.split(dataframe)):
        
        # Save indices
        train_set.append(list(train_index))
        test_set.append(list(test_index))
    
    
    
    df_train = pd.DataFrame( train_set )
    df_test = pd.DataFrame( test_set )
    
    if groups == 1:
        # Save the indexes
        # Use dataset name
        df_train.to_csv( idx_dir + ds.id + "_train.csv", index=False, header = False )
        df_test.to_csv( idx_dir + ds.id + "_test.csv", index=False, header = False )
    elif groups > 1:
        kf = KFold(groups, shuffle=False)
        for i, (_, idx) in enumerate(kf.split(df_train, df_test)):
            sub_train = df_train.iloc[idx,:]
            sub_test = df_test.iloc[idx,:]
            # Save the indexes
            # Use dataset name
            sub_train.to_csv( idx_dir + ds.id + "_train_"+str(i)+".csv", index=False, header = False )
            sub_test.to_csv( idx_dir + ds.id + "_test_"+str(i)+".csv", index=False, header = False )
            
            
    