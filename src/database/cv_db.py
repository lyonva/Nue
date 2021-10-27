from sklearn.model_selection import *
from comp.LoaderCV import LoaderCV
from comp.BootstrapCV import BootstrapCV

cv_db = { "repeatedkfold" : RepeatedKFold,
         "leaveoneout" : LeaveOneOut,
         "loo" : LeaveOneOut,
         "kfold" : KFold,
         "shufflesplit" : ShuffleSplit,
         "repeatedtraintest" : ShuffleSplit,
         "traintestsplit" : ShuffleSplit,
         "loader" : LoaderCV,
         "bootstrap" : BootstrapCV}
