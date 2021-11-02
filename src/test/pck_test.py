# From https://stackoverflow.com/questions/25827160/importing-correctly-with-pytest
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
import pytest

# Uncomment when you have no idea what is failing
# Or if you need to test everything
# from baseline import *
# from dimensionality import *
# from evaluation import *
# from learning import *
# from pipeline import *
# from reading import *
# from selection import *
# from transformation import *
# from tuning import *
# from validation import *


def test_imports():
    """
        Test Imports
        Tests that every importable class works, and can be imported from the package
        Should be updated as more classes are added
    """

    # Baseline package
    from baseline import baseline
    from baseline import marp0
    from baseline import marp0loo
    from baseline import mdarp0
    from baseline import median

    # Dimensionality package
    from dimensionality import Solver

    # Evaluation/Metrics package
    from evaluation import Evaluation
    from evaluation import get_pareto_front

    # Learning package
    from learning import Learner
    from learning import MLPReg

    # Pipeline package
    from pipeline import FeatureJoin

    # Reading/IO package
    from reading import Dataset
    from reading import Loader
    from reading import LoaderCV

    # Selection package
    from selection import FeatureSelection
    from selection import ColumnSelector
    from selection import NumericalSelector
    from selection import AttributeSelector
    from selection import VariantThreshold

    # Transformation package
    from transformation import DataTransformation
    from transformation import OneHotEncoding
    from transformation import FillImputer
    from transformation import SimplerImputer
    from transformation import KNNImputerDF
    from transformation import Missing_Value_Handling
    from transformation import Preprocessing

    # Tuning package
    from tuning import Parameter_Tuning
    from tuning import DefaultCV
    from tuning import BayesianOptimizationCV
    from tuning import DifferentialEvolutionCV
    from tuning import DodgeCV
    from tuning import GeneticAlgorithmCV
    from tuning import HarmonySearchCV
    from tuning import HyperbandCV
    from tuning import NeverGradCV
    from tuning import RandomRangeSearchCV
    from tuning import TabuSearchCV

    # Validation package
    from validation import Cross_Validation
    from validation import BootstrapCV
    from validation import KFold
    from validation import NxM
    from validation import TestCV
