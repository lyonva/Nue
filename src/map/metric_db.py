from evaluation import Metric
from evaluation.formulas.formulas_effort import sdar
from map import DatabaseNoClass
from evaluation.formulas import mar, mdar, sa, effect_size
from sklearn.metrics import accuracy_score

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
            "formula" : lambda x, y, z: accuracy_score(y, z),
            "problem" : "classification",
            "greater_is_better" : True,
            "lo" : 0,
            "hi" : 1,
            "baseline" : "None"
        },
    }
)
