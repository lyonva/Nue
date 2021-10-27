from comp.Baseline import Baseline
import numpy as np

class MDARP0(Baseline):
    
    def fit(self, actual):
        res = 0
        std = 0
        n = actual.size
        actual = np.array(actual)
        
        samples = []
        for i in range(0, n):
            p = [0 if x == i else 1/(actual.size - 1) for x in range(actual.size)]
            pred = np.random.choice(actual, self.n_runs, replace=True, p=p)
            samples.extend( np.abs( actual[i] - pred))
            
        res = np.median(samples)
        std = np.std(samples)
            
        return res, std
    
    