from abc import ABC, abstractmethod

class Baseline(ABC):
    
    def __init__(self, n_runs = 1000):
        self.n_runs = n_runs
    
    @abstractmethod
    def fit(self, actual):
        pass
    