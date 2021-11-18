from evaluation import MetricScorer
from sklearn.metrics import accuracy_score, precision_score,\
    recall_score, f1_score

class Accuracy(MetricScorer):
    
    def setConstants(self):
        self.name = "accuracy"
        self.problem = "classification"
        self.greater_is_better = True
        self.lo = 0
        self.hi = 1
        self.baseline = None
        self.unifeature = False
        self.composite = None
    
    def _score_func(self, y_true, y_pred, X, estimator):
        return accuracy_score( y_true, y_pred )
    

class Precision(MetricScorer):
    
    def setConstants(self):
        self.name = "precision"
        self.problem = "classification"
        self.greater_is_better = True
        self.lo = 0
        self.hi = 1
        self.baseline = None
        self.unifeature = False
        self.composite = None
        self.zero_division = 0
    
    def _score_func(self, y_true, y_pred, X, estimator):
        return precision_score( y_true, y_pred, zero_division = self.zero_division )

class Recall(MetricScorer):
    
    def setConstants(self):
        self.name = "recall"
        self.problem = "classification"
        self.greater_is_better = True
        self.lo = 0
        self.hi = 1
        self.baseline = None
        self.unifeature = False
        self.composite = None
        self.zero_division = 0
    
    def _score_func(self, y_true, y_pred, X, estimator):
        return recall_score( y_true, y_pred, zero_division = self.zero_division )

class F1(MetricScorer):
    
    def setConstants(self):
        self.name = "f1"
        self.problem = "classification"
        self.greater_is_better = True
        self.lo = 0
        self.hi = 1
        self.baseline = None
        self.unifeature = False
        self.composite = None
        self.zero_division = 0
    
    def _score_func(self, y_true, y_pred, X, estimator):
        return f1_score( y_true, y_pred, zero_division = self.zero_division )
