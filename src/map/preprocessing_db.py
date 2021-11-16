from map import Database
from preprocessing import PreProcessor
from preprocessing import FairSmoteSelector, DummyProcessor

preprocessing_db = Database(PreProcessor,
    {
        "none" : DummyProcessor,
        "fairsmote" : FairSmoteSelector,
    },
    {
        "fairsmote" : {
            "secondary" : True,
        },
    }
)