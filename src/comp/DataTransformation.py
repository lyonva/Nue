import pandas as pd
from sklearn.preprocessing import OneHotEncoder

class DataTransformation:
    
    def __init__(self, name = "None", dt_class = None, parameters = {}):
        self.name = name
        self.dt_class = dt_class
        self.parameters = parameters

class OneHotEncoding(OneHotEncoder):
    def transform(self, X):
        res = super().transform(X)
        return pd.DataFrame(res, columns=self.get_feature_names(X.columns))
