from evaluation import Metric, Accuracy, Precision, Recall, F1, FalseAlarm, \
    AOD, EOD, SPD, DI, FR, D2H, MAR, SA, SD, SDAR, EFFECTSIZE, MMRE, PRED25
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
        "sdar" : { "class" : SDAR },
        "effect size" : { "class" : EFFECTSIZE },
        "mmre" : { "class" : MMRE },
        "pred25" : { "class" : PRED25 },
        
        # Classification
        "accuracy" : { "class" : Accuracy },
        "precision" : { "class" : Precision },
        "recall" : { "class" : Recall },
        "f1" : { "class" : F1 },
        "falsealarm" : { "class" : FalseAlarm },
        
        # Fairness
        "aod" : { "class" : AOD },
        "eod" : { "class" : EOD },
        "spd" : { "class" : SPD },
        "di" : { "class" : DI },
        "fr" : { "class" : FR },
    }
)
