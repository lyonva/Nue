from evaluation import MetricX
from sklearn.metrics import confusion_matrix

def slice_privilege(X):
    """
    Function:
        slice_privilege
    Description:
        Returns 2 masks, i.e. lists of booleans.
        Indicating if index corresponds with (un)privileged class.
        We assume privilege classes are 0 in the data.
    Input:
        - X,dataframe: Columns that the model predicted on.
        - feature,str: Name of the feature.
    Output:
        2 lists of booleans.
        First is mask of privileged class.
        Second is mask for unprivileged class.
    """
    return X == 0, X == 1

def get_confusion(y_true, y_pred, X):
    """
    Function:
        get_confusion
    Description:
        Calculates confusion matrix of (un)priviledged class.
    Input:
        - y_true,list: List of actual y values.
        - y_pred,list: List of predicted y values.
        - X,dataframe: Columns that the model predicted on.
        - feature,str: Name of the feature.
    Output:
        2 tiered dictionary with this structure:
        {
            "priv" : {
                "tp" : tp,
                "tn" : tn,
                "fp" : fp,
                "fn" : fn
            },
            "unpr" : {
                "tp" : tp,
                "tn" : tn,
                "fp" : fp,
                "fn" : fn
            },
        }
    """
    priv, unpriv = slice_privilege(X)
    priv_true, priv_pred = y_true[priv], y_pred[priv]
    unpr_true, unpr_pred = y_true[unpriv], y_pred[unpriv]
    
    res = {}
    for name, true, pred in zip( ["priv", "unpr"], [priv_true, unpr_true], [priv_pred, unpr_pred] ):
        tn, fp, fn, tp = confusion_matrix(true, pred).ravel()
        res[name] = {
            "tp" : tp,
            "tn" : tn,
            "fp" : fp,
            "fn" : fn
        }
    return res
    

class AOD(MetricX):
    """
    Class:
        AOD
    Description:
        MetricX of Average Odds Difference
        Average of difference in False Positive Rates(FPR)
        and True Positive Rates(TPR) for unprivileged and privileged groups.
    """
    
    def setConstants(self):
        self.name = "aod"
        self.problem = "classification"
        self.greater_is_better = True
        self.lo = 0
        self.hi = 1
        self.baseline = None
    
    def _score_func(self, y_true, y_pred, X):
        conf = get_confusion(y_true, y_pred, X)
        tpr_unpr = conf["unpr"]["tp"]/( conf["unpr"]["tp"] + conf["unpr"]["fn"] )
        fpr_unpr = conf["unpr"]["fp"]/( conf["unpr"]["fp"] + conf["unpr"]["tn"] )
        tpr_priv = conf["priv"]["tp"]/( conf["priv"]["tp"] + conf["priv"]["fn"] )
        fpr_priv = conf["priv"]["fp"]/( conf["priv"]["fp"] + conf["priv"]["tn"] )
        return ((fpr_unpr - fpr_priv) + (tpr_unpr - tpr_priv)) / 2


class EOD(MetricX):
    """
    Class:
        EOD
    Description:
        MetricX of Equal Opportunity Difference
        Difference of True Positive Rates(TPR) for unprivileged and privileged groups.
    """
    
    def setConstants(self):
        self.name = "eod"
        self.problem = "classification"
        self.greater_is_better = True
        self.lo = 0
        self.hi = 1
        self.baseline = None
    
    def _score_func(self, y_true, y_pred, X):
        conf = get_confusion(y_true, y_pred, X)
        tpr_unpr = conf["unpr"]["tp"]/( conf["unpr"]["tp"] + conf["unpr"]["fn"] )
        tpr_priv = conf["priv"]["tp"]/( conf["priv"]["tp"] + conf["priv"]["fn"] )
        return tpr_unpr - tpr_priv
