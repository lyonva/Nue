from utils import ps, get_problem_type
from map import baseline_db
from sklearn.metrics import make_scorer

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
            Instances a Learner, storing name, class, and default parameters.
        Input:
            - name,str: Name of metric
            - formula,callable: Function of form f(self, y, y_pred) that returns something.
            - problem,str: Whether metric is for classification, regression, or both.
            - greater_is_better,bool: Whether a learner/optimizer should increase this metric or not.
            - lo,float or None: Reference point, theorethical lowest possible value.
            - hi,float or None: Reference point, theorethical highest possible value.
            - baseline,str: Baseline object name to calculate this metric.
        Output:
            Instance of the Learner.
        """
        self.name = name
        self.formula = formula
        self.greater_is_better = greater_is_better
        self.problem = get_problem_type(problem)
        self.lo = lo
        self.hi = hi
        self.baseline = baseline_db[baseline]
    
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
        return lambda y, y_pred : self.formula(self, y, y_pred)
    
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
    
    def evaluate( self, y, y_pred ):
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
