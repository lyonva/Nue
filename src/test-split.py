# Libraries
import numpy as np
import pandas as pd

from database.dataset_db import dataset_db
from database.cv_db import cv_db
from comp.Loader import Loader
from sklearn.model_selection import KFold

# Prelude
data_dir = "data/"
groups = 10 # Partition the indexes into different datasets? For multiple PCs

# Load configuration
FW, DS, DT, AS, PT, LA, EM = Loader().load_config()
datasets = dataset_db.get(DS)

# Cross Validation
# Defaults to 80:20 train test split
#cv = cv_db[ FW["cv"][0] if "cv" in FW.keys() else "traintestsplit" ]( **(FW["cv"][1] if "cv" in FW.keys() else {"n_splits":1, "test_size":0.2}) )
cv = (cv_db["traintestsplit"])(n_splits=1, test_size=0.1)

# Dataset Loop
for ds in datasets:
    ds.set_datapath("data/")
    dataframe = ds.get_dataframe()
    
    # Data pre-processing
    # dataframe = prep.process(dataframe)
    
    # Cross validation
    for train_index, test_index in cv.split(dataframe):
        
        # Save indices
        train_set = dataframe.iloc[train_index,:]
        test_set = dataframe.iloc[test_index,:]
    
        # Save the indexes
        # Use dataset name
        train_set.to_csv( data_dir + ds.id + "_train.csv", index=False )
        test_set.to_csv( data_dir + ds.id + "_test.csv", index=False )
            
    