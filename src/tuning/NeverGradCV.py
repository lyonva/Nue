from sklearn.model_selection._search import BaseSearchCV
import numpy as np
from tuning import grid_to_bounds, grid_types, cast_parameters, aggregate_dict
import pandas as pd
from sklearn.model_selection import train_test_split
import nevergrad as ng

# Generic interface for a NeverGrad algorithm
# Controlled using the method parameter
# The name is searched in the optimizer registry
# https://github.com/FacebookResearch/Nevergrad
# Adapted to the scikit learn BaseSearchCV class
class NeverGradCV(BaseSearchCV):
    def __init__(self, estimator, search_space, method, budget, *, scoring=None, n_jobs=None,
                 refit=True, cv=None, verbose=0,
                 pre_dispatch='2*n_jobs', error_score=np.nan, return_train_score=True, **kwargs):
        super().__init__(
            estimator=estimator, scoring=scoring,
            n_jobs=n_jobs, refit=refit, cv=cv, verbose=verbose,
            pre_dispatch=pre_dispatch, error_score=error_score,
            return_train_score=return_train_score)
        self.search_space = search_space
        self.method = method
        self.budget = budget
        self.other_args = kwargs
    
    def _run_search(self, evaluate_candidates):
        self.rank_test_name_ = "rank_test_" + self.refit if self.multimetric_ else "rank_test_score"
        self.mean_test_name_ = "mean_test_" + self.refit if self.multimetric_ else "mean_test_score"
        self.scoring_sign_ = self.scoring[self.refit]._sign if self.multimetric_ else self.scoring._sign
        
        bounds = grid_to_bounds(self.search_space)
        categories = dict( [ (k,v) for k,v in self.search_space.items() if k not in bounds.keys() ] )
        types = grid_types(self.search_space)
        
        search_space = dict( [ (key, ng.p.Scalar( lower=val[0], upper=val[1] ) ) for key, val in bounds.items() ] )
        for key, val in search_space.items():
            if types[key] in [np.int64, np.int32, int]: search_space[key] = val.set_integer_casting()
        for key, val in categories.items(): search_space[key] = ng.p.Choice( val )
        parametrization = ng.p.Instrumentation( **search_space )
        
        tuner = ng.optimizers.registry[self.method](parametrization=parametrization, budget=self.budget, **self.other_args)
        def opt_fun(**kwargs):
            res = evaluate_candidates( [kwargs] ) [self.mean_test_name_][-1] * self.scoring_sign_ * -1
            return res
        # opt_fun = lambda **kwargs : evaluate_candidates( [kwargs] ) [self.mean_test_name_][-1] * self.scoring_sign_ * -1
        tuner.minimize( opt_fun )
        
        