from comp.FeatureSelection import *
from sklearn.feature_extraction import *

# Filters
ds_kbest = FeatureSelection( SelectKBest, False )
ds_precentile = FeatureSelection( SelectPercentile, False )