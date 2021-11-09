from evaluation import Metric
from map import DatabaseNoClass
from evaluation.formulas import mar, mdar, sa, effect_size
from sklearn.metrics import accuracy_score, precision_score,\
    recall_score, f1_score

def warpTwoArg(f):
    return lambda x, y : f(x, y)

metric_db = DatabaseNoClass(
    Metric,
    {
        # Effort estimation
        "mar" : {
            "formula" : mar,
            "problem" : "regression",
            "greater_is_better" : False,
            "lo" : 0,
            "hi" : None,
            "baseline" : "None"
        },
        "mdar" : {
            "formula" : mdar,
            "problem" : "regression",
            "greater_is_better" : False,
            "lo" : 0,
            "hi" : None,
            "baseline" : "None"
        },
        "sa" : {
            "formula" : sa,
            "problem" : "regression",
            "greater_is_better" : True,
            "lo" : -1,
            "hi" : 1,
            "baseline" : "marp0"
        },
        "effect_size" : {
            "formula" : effect_size,
            "problem" : "regression",
            "greater_is_better" : True,
            "lo" : 0,
            "hi" : 1,
            "baseline" : "marp0"
        },
        
        # Classification
        "accuracy" : {
            "formula" : warpTwoArg(accuracy_score),
            "problem" : "classification",
            "greater_is_better" : True,
            "lo" : 0,
            "hi" : 1,
            "baseline" : "None"
        },
        "precision" : {
            "formula" : warpTwoArg(precision_score),
            "problem" : "classification",
            "greater_is_better" : True,
            "lo" : 0,
            "hi" : 1,
            "baseline" : "None"
        },
        "recall" : {
            "formula" : warpTwoArg(recall_score),
            "problem" : "classification",
            "greater_is_better" : True,
            "lo" : 0,
            "hi" : 1,
            "baseline" : "None"
        },
        "f1" : {
            "formula" : warpTwoArg(f1_score),
            "problem" : "classification",
            "greater_is_better" : True,
            "lo" : 0,
            "hi" : 1,
            "baseline" : "None"
        }
    }
)
