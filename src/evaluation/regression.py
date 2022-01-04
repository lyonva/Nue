from evaluation import MetricScorer
from .formulas import mar, sa, sd, sdar
from baseline import MARP0

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
        return mar(self, y_true, y_pred)

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