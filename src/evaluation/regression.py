from evaluation import MetricScorer
from .formulas import mar, sa, sd, sdar, effect_size, mmre, pred25
from baseline import MARP0
from sklearn import metrics
import numpy as np

class MAR(MetricScorer):
    
    def setConstants(self):
        self.name = "mar"
        self.problem = "regression"
        self.greater_is_better = False
        self.lo = 0
        self.hi = 20000 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        return mar(self, y_true, y_pred)

class SDAR(MetricScorer):
    
    def setConstants(self):
        self.name = "sdar"
        self.problem = "regression"
        self.greater_is_better = False
        self.lo = 0
        self.hi = 200000 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        return sdar(self, y_true, y_pred)

class SA(MetricScorer):
    
    def setConstants(self):
        self.name = "sa"
        self.problem = "regression"
        self.greater_is_better = True
        self.lo = 0
        self.hi = 1 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        return sa(self, y_true, y_pred)

class SD(MetricScorer):
    
    def setConstants(self):
        self.name = "sd"
        self.problem = "regression"
        self.greater_is_better = True
        self.lo = 0
        self.hi = 1 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        return sd(self, y_true, y_pred)

class EFFECTSIZE(MetricScorer):
    def setConstants(self):
        self.name = "effect size"
        self.problem = "regression"
        self.greater_is_better = True
        self.lo = 0
        self.hi = 1 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        return effect_size(self, y_true, y_pred)

class MMRE(MetricScorer):
    def setConstants(self):
        self.name = "mmre"
        self.problem = "regression"
        self.greater_is_better = False
        self.lo = 0
        self.hi = 20000 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        return mmre(self, y_true, y_pred)

class PRED25(MetricScorer):
    def setConstants(self):
        self.name = "pred25"
        self.problem = "regression"
        self.greater_is_better = True
        self.lo = 0
        self.hi = 1 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        return pred25(self, y_true, y_pred)

class MAE(MetricScorer):
    def setConstants(self):
        self.name = "mae"
        self.problem = "regression"
        self.greater_is_better = False
        self.lo = 0
        self.hi = 10000 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        mae = metrics.mean_absolute_error(y_true, y_pred)
        return mae

class MSE(MetricScorer):
    def setConstants(self):
        self.name = "mse"
        self.problem = "regression"
        self.greater_is_better = False
        self.lo = 0
        self.hi = 5000000 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        mse = metrics.mean_squared_error(y_true, y_pred)
        return mse

class RMSE(MetricScorer):
    def setConstants(self):
        self.name = "rmse"
        self.problem = "regression"
        self.greater_is_better = False
        self.lo = 0
        self.hi = 10000 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        rmse = np.sqrt(metrics.mean_squared_error(y_true, y_pred))
        return rmse

class MAPE(MetricScorer):
    def setConstants(self):
        self.name = "mape"
        self.problem = "regression"
        self.greater_is_better = False
        self.lo = 0
        self.hi = 1000 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        mape = np.mean(np.abs((y_true - y_pred) / np.abs(y_true)))
        mape = round(mape * 100, 2)
        return mape

class RegressionAccuracy(MetricScorer):
    def setConstants(self):
        self.name = "regression_accuracy"
        self.problem = "regression"
        self.greater_is_better = True
        self.lo = -1000
        self.hi = 100 # Not really, but upped bound is infinity
        self.baseline = MARP0
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X=None, estimator=None):
        mape = np.mean(np.abs((y_true - y_pred) / np.abs(y_true)))
        acc = round(100*(1 - mape), 2)
        return acc