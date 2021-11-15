import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from utils import ps

class DataTransformation(ps):
    
    def __init__(self, name = "None", dt_class = None, parameters = {}):
        self.name = name
        self.dt_class = dt_class
        self.parameters = parameters

class OneHotEncoding(OneHotEncoder):
    def transform(self, X):
        res = super().transform(X)
        return pd.DataFrame(res, columns=self.get_feature_names_out(X.columns))

class StandardScaling(StandardScaler):
    def transform(self, X, copy=None):
        return pd.DataFrame( super().transform(X), columns=X.columns )

class MinMaxScaling(MinMaxScaler):
    def transform(self, X, copy=None):
        return pd.DataFrame( super().transform(X), columns=X.columns )
