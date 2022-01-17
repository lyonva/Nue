from map import Database
from modeling import Model, XOMOModel

model_db = Database(Model,
            {
                "xomo" : XOMOModel
            },
            {
                "xomo" : { }
            }
    
)
