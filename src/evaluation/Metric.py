from utils import ps, get_problem_type
from sklearn.metrics import make_scorer
from inspect import signature
from abc import ABC, abstractmethod
from sklearn.metrics._scorer import _PredictScorer

# Local baseline DB
# To avoid circular imports
from baseline import MARP0
from baseline import MDARP0
from baseline import Median
from baseline import MARP0LOO

baselines = { "None" : None,
         "marp0" : MARP0(),
         "mdarp0" : MDARP0(),
         "median" : Median(),
         "marp0loo" : MARP0LOO()
}


class Metric(ps):
    """
    Class:
        Metric
    Description:
        Represents an evaluation metric.
        Functions for both regression and optimization.
    Attributes:
        - name,str: Name of metric
        - formula,callable: Function that returns something.
            Takes the form: f(self, y, y_pred)
        - problem,str: Whether metric is for classification, regression, or both.
        - greater_is_better,bool: Whether a learner/optimizer should increase this metric or not.
        - lo,float or None: Reference point, theorethical lowest possible value.
        - hi,float or None: Reference point, theorethical highest possible value.
        - baseline,class: Baseline object to calculate this metric.
    """

    def __init__(self,  name, *, formula = None, problem = "none",
                greater_is_better = False, lo = None, hi = None, baseline = "None"):
        """
        Function:
            __init__
        Description:
            Instances a Metric, storing all attributes.
        Input:
            - name,str: Name of metric
            - formula,callable: Function of form f(self, y, y_pred) that returns something.
            - problem,str: Whether metric is for classification, regression, or both.
            - greater_is_better,bool: Whether a learner/optimizer should increase this metric or not.
            - lo,float or None: Reference point, theorethical lowest possible value.
            - hi,float or None: Reference point, theorethical highest possible value.
            - baseline,str: Baseline object name to calculate this metric.
        Output:
            Instance of the Metric.
        """
        self.name = name
        self.formula = formula
        self.greater_is_better = greater_is_better
        self.problem = get_problem_type(problem)
        self.lo = lo
        self.hi = hi
        self.baseline = baselines[baseline]
    
    def get_formula(self):
        """
        Function:
            get_formula
        Description:
            Returns function in the form f(y, y_pred).
            This is done so certain functions have access to baseline.
        Input:
            None
        Output:
            callable
        """
        n_args = len(signature(self.formula).parameters)
        if n_args < 2:
            return None
        elif n_args == 2:
            return self.formula
        elif n_args == 3:
            return lambda y, y_pred : self.formula(self, y, y_pred)
        else:
            return None
    
    def make_scorer(self):
        """
        Function:
            make_scorer
        Description:
            Returns a scikit_learn scorer.
            Done to train models.
        Input:
            None
        Output:
            callable, for use by sklearn.
        """
        return make_scorer( self.get_formula(), greater_is_better = self.greater_is_better )
    
    def evaluate( self, y, y_pred, **kwargs ):
        """
        Function:
            evaluate
        Description:
            Calculates a metric form a given input.
        Input:
            - y,list: List of the true y values
            - y_pred,list: List of predicted y values
        Output:
            Float value of the metric.
        """
        return self.get_formula()(y, y_pred)


class MetricX(ABC, Metric, _PredictScorer):
    """
    Class:
        MetricX
    Description:
        Abstract class, requires definition of score method
        Represents an evaluation metric that requires a dataset column.
        Made as a scikit learn scorer.
    Attributes:
        - feature,str: name of feature to calculate metric.
    Constants: Should be set by constructor of each subclass
        - name,str: Name of metric
        - problem,str: Whether metric is for classification, regression, or both.
        - greater_is_better,bool: Whether a learner/optimizer should increase this metric or not.
        - lo,float or None: Reference point, theorethical lowest possible value.
        - hi,float or None: Reference point, theorethical highest possible value.
        - baseline,class: Baseline object to calculate this metric.
    """
    
    def __init__(self, name = None, feature = None):
        """
        Function:
            __init__
        Description:
            Instances a MetricX, storing all attributes.
        Input:
            - name,str: Unused
            - feature,str: name of feature to calculate metric.
        Output:
            Instance of the MetricX.
        """
        self.feature = feature
        self.setConstants()
        if feature != None:
            self.name += "-" + feature
        self._sign = 1 if self.greater_is_better else -1
        self._kwargs = {}
    
    def make_scorer(self):
        """
        Function:
            make_scorer
        Description:
            Returns a scikit_learn scorer.
            As we are one, return self.
        Input:
            None
        Output:
            self
        """
        return self
    
    @abstractmethod
    def setConstants(self):
        """
        Function:
            setConstants
        Description:
            Sets the constants of the MetriX.
            Should be implemented by each subclass.
            This is a template.
        Input:
            None.
        Output:
            None. Should modify attributes.
        """
        self.name = ""
        self.problem = None
        self.greater_is_better = None
        self.lo = None
        self.hi = None
        self.baseline = None
    
    def _score(self, method_caller, estimator, X, y_true, sample_weight=None):
        """
        Function:
            _score
        Description:
            Scikit learn score.
            We override it to be able to access X as we calculate the metric.
            Description from scikit-learn:
         
        Evaluate predicted target values for X relative to y_true.
        Parameters
        ----------
        method_caller : callable
            Returns predictions given an estimator, method name, and other
            arguments, potentially caching results.
        estimator : object
            Trained estimator to use for scoring. Must have a `predict`
            method; the output of that is used to compute the score.
        X : {array-like, sparse matrix}
            Test data that will be fed to estimator.predict.
        y_true : array-like
            Gold standard target values for X.
        sample_weight : array-like of shape (n_samples,), default=None
            Sample weights.
        Returns
        -------
        score : float
            Score function applied to prediction of estimator on X.
        """

        y_pred = method_caller(estimator, "predict", X)
        if sample_weight is not None:
            return self._sign * self._score_func(
                y_true, y_pred, X[self.feature], sample_weight=sample_weight, **self._kwargs
            )
        else:
            return self._sign * self._score_func(y_true, y_pred, X[self.feature], **self._kwargs)
    
    @abstractmethod
    def _score_func(self, y_true, y_pred, X):
        """
        Function:
            _score_func
        Description:
            Calculate and return the metric.
        Input:
            - y_true,list: List of actual y values.
            - y_pred,list: List of predicted y values.
            - X,dataframe: Columns that the model predicted on.
        Output:
            None. Should modify attributes.
        """
        pass
    
    def evaluate(self, y, y_pred, X = None):
        return self._score_func(y, y_pred, X[self.feature])
