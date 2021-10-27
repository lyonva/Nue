from comp.DataTransformation import DataTransformation
from scipy.stats import boxcox
from numpy import log, mean, std
from database.Database import Database
from sklearn.preprocessing import StandardScaler, FunctionTransformer
import pandas as pd
import numpy as np

#"none":lambda x: x,
#"log":log,
#"boxcox":boxcox,
#"norm" : lambda x : (x - mean(x))/std(x)

class StandardScaler2(StandardScaler):
    def transform(self, X, copy=None):
        return pd.DataFrame( super().transform(X), columns=X.columns )
    
    

dt_db = Database(DataTransformation, {"none" : FunctionTransformer,
                                      "norm" : StandardScaler2,
                                      "log" : FunctionTransformer
                                      },
                                     {"log" : {"func":np.log1p,
                                               "inverse_func":np.expm1
                                               },
                                      })
