from map import Database
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from optimization import Optimizer, DefaultCV, DifferentialEvolutionCV, FlashCV, DodgeCV, \
    RandomRangeSearchCV, NeverGradCV, TabuSearchCV, HarmonySearchCV, HyperbandCV, \
    GeneticAlgorithmCV, BayesianOptimizationCV


# class DummyPT:
#     def __init__(self, estimator, param_distributions, **params):
#         self.estimator = estimator
#         self.param_distributions = param_distributions
#         self.best_params_ = {}
    
#     def fit(self, X, Y, **fit_params):
#         self.estimator.fit(X, Y, **fit_params)
#         return self
#     def predict(self, X):
#         return self.estimator.predict(X)
#     def transform(self, X):
#         return self.estimator.transform(X)
    
#     def get_params(self):
#         return self.estimator.get_params()
    
    
    
    
optimization_db = Database(Optimizer, {"none":DefaultCV,
                                        "default":DefaultCV,
                                        "grid search":GridSearchCV,
                                        "random search":RandomizedSearchCV,
                                        "random range search":RandomRangeSearchCV,
                                        "de":DifferentialEvolutionCV,
                                        "flash":FlashCV,
                                        "dodge":DodgeCV,
                                        "oneplusone":NeverGradCV,
                                        "cga":NeverGradCV,
                                        "pso":NeverGradCV,
                                        "bo":BayesianOptimizationCV,
                                        "tabu":TabuSearchCV,
                                        "harmony":HarmonySearchCV,
                                        "hyperband":HyperbandCV,
                                        "ga":GeneticAlgorithmCV
                                        },
                                     {"grid search":{"n_jobs":-1},
                                         "random search":{"n_jobs":-1},
                                         "random range search":{"n_jobs":-1},
                                         "de":{"n_jobs":-1},
                                         "flash":{"n_jobs":-1},
                                         "dodge":{"n_jobs":-1},
                                         "oneplusone":{"n_jobs":-1, "method":"OnePlusOne"},
                                         "cga":{"n_jobs":-1, "method":"cGA"},
                                         "pso":{"n_jobs":-1, "method":"PSO"},
                                         "bo":{"n_jobs":-1},
                                         "tabu":{"n_jobs":-1},
                                         "harmony":{"n_jobs":-1},
                                         "hyperband":{"n_jobs":-1},
                                         "ga":{"n_jobs":-1}
                                         })
