from map import Database
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.dummy import DummyRegressor
from learning import Learner
from learning import MLPReg


learning_db = Database(Learner,
                  {"knn":KNeighborsRegressor,
                    "mlp":MLPReg,
                    "multilayerperceptron":MLPReg,
                    "mlp-sigmoid":MLPReg,
                    "mlp-tanh":MLPReg,
                    "mlp-relu":MLPReg,
                    "lr":LinearRegression,
                    "ols":LinearRegression,
                    "linearregression":LinearRegression,
                    "gp":GaussianProcessRegressor,
                    "gaussianprocesses":GaussianProcessRegressor,
                    "ridgeregression":Ridge,
                    "ridge":Ridge,
                    "svr":SVR, "svm":SVR, "smoreg":SVR,
                    "svr-rbf":SVR,
                    "svr-poly":SVR,
                    "svr-sigmoid":SVR,
                    "additiveregression":GaussianProcessRegressor,
                    "bagging":BaggingRegressor,
                    "zeror":DummyRegressor,
                    "decisionstump":DecisionTreeRegressor,
                    "reptree":DecisionTreeRegressor,
                    "regressiontree":DecisionTreeRegressor
                    },
                  {"decisionstump":{"max_depth",1} ,
                   "additiveregression":{"max_depth",1},
                   "bagging":{"base_estimator",DecisionTreeRegressor(max_depth = 1)},
                   "mlp-sigmoid":{"activation":"logistic"},
                   "mlp-tanh":{"activation":"tanh"},
                   "mlp-relu":{"activation":"relu"},
                   "svr-rbf":{"kernel":"rbf"},
                   "svr-poly":{"kernel":"poly"},
                   "svr-sigmoid":{"kernel":"sigmoid"}
                   })
