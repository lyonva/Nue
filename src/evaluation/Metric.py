from utils import ps, get_problem_type
from map import baseline_db

class Metric(ps):
    """
    Class:
        Metric
    Description:
        Represents an evaluation metric.
        Functions for both regression and optimization.
    Attributes:
        - name,str: Name of metric
        - formula,callable: Function that returns something. Can take multiple forms:
            - Normal: f(pred, actual)
            - Baseline: f(pred, actual, baseline)
        - problem,str: Whether metric is for classification, regression, or both.
        - greater_is_better,bool: Whether a learner/optimizer should increase this metric or not.
        - floor,float: Theorethical lowest possible value.
        - baseline,class: Baseline object to calculate this metric.
    """

    def __init__(self,  name, *, formula = None, problem = "none",
                greater_is_better = False, floor = None, baseline = "None"):
        """
        Function:
            __init__
        Description:
            Instances a Learner, storing name, class, and default parameters.
        Input:
            - name,str: Name of metric
            - formula,callable: Function of form f(pred, actual) that returns something.
            - problem,str: Whether metric is for classification, regression, or both.
            - greater_is_better,bool: Whether a learner/optimizer should increase this metric or not.
            - floor,float: Theorethical lowest possible value.
            - baseline,str: Baseline object name to calculate this metric.
        Output:
            Instance of the Learner.
        """
        self.name = name
        self.formula = formula
        self.greater_is_better = greater_is_better
        self.problem = get_problem_type(problem)
        self.floor = floor
        self.baseline = baseline_db[baseline]

