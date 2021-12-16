from evaluation import Metric, Accuracy, Precision, Recall, F1,\
    AOD, EOD, SPD, DI, FR, D2H, MAR, SA, SD
from map import DatabaseNoClass
from evaluation.formulas import mar, mdar, sa, effect_size

metric_db = DatabaseNoClass(
    {
        # Generic
        "d2h" : {
            "class" : D2H,
        },
        
        # Effort estimation
        "mar" : { "class" : MAR },
        "sa" : { "class" : SA },
        "sd" : { "class" : SD },
        
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
