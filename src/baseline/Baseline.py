from abc import ABC, abstractmethod

class Baseline(ABC):
    """
    Class:
        Baseline
    Description:
        Abstract class.
        Baseline prediction algorithms.
        Very simple, used for the calculation of metrics.
    Attributes:
        - n_runs,int: If baseline is stochastic, amount of repetitions
    """
    def __init__(self, n_runs = 1000):
        self.n_runs = n_runs
    
    @abstractmethod
    def fit(self, actual):
        pass
    