from comp.MARP0 import MARP0
from comp.MDARP0 import MDARP0
from comp.Median import Median
from comp.MARP0LOO import MARP0LOO

bl_db = { "None" : None,
         "marp0" : MARP0(),
         "mdarp0" : MDARP0(),
         "median" : Median(),
         "marp0loo" : MARP0LOO()
         }
