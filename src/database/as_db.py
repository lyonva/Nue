from sklearn.feature_selection import chi2, f_classif, f_regression
from sklearn.feature_selection import SelectKBest, SelectPercentile, SelectFpr, SelectFdr, SelectFwe, RFE, VarianceThreshold
from database.Database import Database
from comp.VariantThreshold import VariantThreshold
from sklearn.ensemble import RandomForestRegressor
from comp.AttributeSelector import AttributeSelector
from boruta import BorutaPy
from sklearn.base import BaseEstimator, TransformerMixin
# =============================================================================
# 
# selection_functions = [chi2, f_classif, f_regression]
# 
# as_kbestparams = {"score_func" : selection_functions, "k" : [5,10,15,20]}
# as_kbest = AttributeSelector("kbest", SelectKBest, as_kbestparams)
# 
# as_percentileparams = {"score_func" : selection_functions, "percentile" : [5,10,15,20]}
# as_percentile = AttributeSelector("percentile", SelectPercentile, as_percentileparams)
# 
# as_fprparams = {"score_func" : selection_functions}
# as_fpr = AttributeSelector("fpr", SelectFpr, as_fprparams)
# 
# as_fdrparams = {"score_func" : selection_functions}
# as_fdr = AttributeSelector("fdr", SelectFdr, as_fdrparams)
# 
# as_fweparams = {"score_func" : selection_functions}
# as_fwe = AttributeSelector("fwe", SelectFwe, as_fweparams)
# =============================================================================

class BorutaPy2(BorutaPy):
    def fit(self, X, y):
        super()._fit( X.values, y.values )
    
    def transform(self, X, weak=False):
        # sanity check
        try:
            self.ranking_
        except AttributeError:
            raise ValueError('You need to call the fit(X, y) method first.')

        if weak:
            indices = self.support_ + self.support_weak_
        else:
            indices = self.support_

        X = X.iloc[:, indices]
        
        return X
    
    def fit_transform(self, X, y, weak=False):
        self.fit(X, y)
        return self.transform(X, weak)

class DummyAS(BaseEstimator, TransformerMixin):
    def fit(self, X, Y, **fit_params):
        return self
    def transform(self, X):
        return X
    def get_params(self, **params):
        return {}

as_db = Database(AttributeSelector, {"none":DummyAS,
                                     "kbest":SelectKBest,
                                     "percentile":SelectPercentile,
                                     "fpr":SelectFpr,
                                     "fdr":SelectFdr,
                                     "fwe":SelectFwe,
                                     "rfe":RFE,
                                     #"variancethreshold":VarianceThreshold,
                                     "variancethreshold":VariantThreshold,
                                     "correlationkbest":SelectKBest,
                                     "correlationpercentile":SelectPercentile,
                                     "randomforest":BorutaPy2,
                                     "boruta":BorutaPy2},
                 {"rfe": {"wrapper":True},
                  "boruta":{"wrapper":True},
                  "correlationkbest":{"score_func":f_regression},
                  "correlationpercentile":{"score_func":f_regression},
                 "randomforest":{"wrapper":False, "estimator":RandomForestRegressor(n_jobs=-1, max_depth=5), "n_estimators":"auto"}
                 })


