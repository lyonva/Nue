class Learner:
    """
    class:
        Learner
    description:
        Represents an scikit-learn object
        Interface adds hyper-parameters for easiness at tuning
        Supports classification/regression
    """
    def __init__(self, name, classification = None, regression = None, parameters = {}):
        self.name = name
        self.classification = classification
        self.regression = regression
        self.parameters = parameters

        # Set the type of problem that this learner supports
        problem = "none"
        if (self.regression != None) and (self.classification != None):
            problem = "both"
        elif (self.regression != None):
            problem = "regression"
        elif (self.classification != None):
            problem = "classification"
        self.problem = problem