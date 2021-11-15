from evaluation import Metric, AOD, EOD, SPD, DI, FR
from map import DatabaseNoClass
from evaluation.formulas import mar, mdar, sa, effect_size
from sklearn.metrics import accuracy_score, precision_score,\
    recall_score, f1_score

metric_db = DatabaseNoClass(
    {
        # Effort estimation
        "mar" : {
            "class" : Metric,
            "formula" : mar,
            "problem" : "regression",
            "greater_is_better" : False,
            "lo" : 0,
            "hi" : None,
            "baseline" : "None"
        },
        "mdar" : {
            "class" : Metric,
            "formula" : mdar,
            "problem" : "regression",
            "greater_is_better" : False,
            "lo" : 0,
            "hi" : None,
            "baseline" : "None"
        },
        "sa" : {
            "class" : Metric,
            "formula" : sa,
            "problem" : "regression",
            "greater_is_better" : True,
            "lo" : -1,
            "hi" : 1,
            "baseline" : "marp0"
        },
        "effect_size" : {
            "class" : Metric,
            "formula" : effect_size,
            "problem" : "regression",
            "greater_is_better" : True,
            "lo" : 0,
            "hi" : 1,
            "baseline" : "marp0"
        },
        
        # Classification
        "accuracy" : {
            "class" : Metric,
            "formula" : accuracy_score,
            "problem" : "classification",
            "greater_is_better" : True,
            "lo" : 0,
            "hi" : 1,
            "baseline" : "None"
        },
        "precision" : {
            "class" : Metric,
            "formula" : precision_score,
            "problem" : "classification",
            "greater_is_better" : True,
            "lo" : 0,
            "hi" : 1,
            "baseline" : "None",
            "zero_division" : 0,
        },
        "recall" : {
            "class" : Metric,
            "formula" : recall_score,
            "problem" : "classification",
            "greater_is_better" : True,
            "lo" : 0,
            "hi" : 1,
            "baseline" : "None",
            "zero_division" : 0,
        },
        "f1" : {
            "class" : Metric,
            "formula" : f1_score,
            "problem" : "classification",
            "greater_is_better" : True,
            "lo" : 0,
            "hi" : 1,
            "baseline" : "None",
            "zero_division" : 0,
        },
        
        # Fairness
        "aod" : { "class" : AOD },
        "eod" : { "class" : EOD },
        "spd" : { "class" : SPD },
        "di" : { "class" : DI },
        "fr" : { "class" : FR },
    }
)
