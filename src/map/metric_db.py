from evaluation import Metric, Accuracy, Precision, Recall, F1,\
    AOD, EOD, SPD, DI, FR, D2H
from map import DatabaseNoClass
from evaluation.formulas import mar, mdar, sa, effect_size

metric_db = DatabaseNoClass(
    {
        # Generic
        "d2h" : {
            "class" : D2H,
        },
        
        # Effort estimation
        # "mar" : {
        #     "class" : Metric,
        #     "formula" : mar,
        #     "problem" : "regression",
        #     "greater_is_better" : False,
        #     "lo" : 0,
        #     "hi" : None,
        #     "baseline" : "None"
        # },
        # "mdar" : {
        #     "class" : Metric,
        #     "formula" : mdar,
        #     "problem" : "regression",
        #     "greater_is_better" : False,
        #     "lo" : 0,
        #     "hi" : None,
        #     "baseline" : "None"
        # },
        # "sa" : {
        #     "class" : Metric,
        #     "formula" : sa,
        #     "problem" : "regression",
        #     "greater_is_better" : True,
        #     "lo" : -1,
        #     "hi" : 1,
        #     "baseline" : "marp0"
        # },
        # "effect_size" : {
        #     "class" : Metric,
        #     "formula" : effect_size,
        #     "problem" : "regression",
        #     "greater_is_better" : True,
        #     "lo" : 0,
        #     "hi" : 1,
        #     "baseline" : "marp0"
        # },
        
        # Classification
        "accuracy" : { "class" : Accuracy },
        "precision" : { "class" : Precision },
        "recall" : { "class" : Recall },
        "f1" : { "class" : F1 },
        
        # Fairness
        "aod" : { "class" : AOD },
        "eod" : { "class" : EOD },
        "spd" : { "class" : SPD },
        "di" : { "class" : DI },
        "fr" : { "class" : FR },
    }
)
