from comp.Baseline import Baseline
import numpy as np

class Median(Baseline):
    
    def fit(self, actual):
        res = 0
        std = 0
        n = actual.size
        actual = np.array(actual)
        
        prediction = np.median(actual)
        samples = np.abs( actual - prediction )
        
        res = np.mean(samples)
        std = np.std(samples)
            
        return res, std
    
    