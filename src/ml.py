# Libraries
import numpy as np
import pandas as pd

from map import dataset_db as ds_db
from map import transformation_db as dt_db
from map import selection_db as as_db
from map import learning_db as mlt_db
from map import optimization_db as pt_db
from map import baseline_db as bl_db
from map import validation_db as cv_db
from sklearn.metrics import make_scorer
from reading import Loader
from validation import LoaderCV
from evaluation import Evaluation
from transformation import Preprocessing
from joblib import Memory
from shutil import rmtree
from tempfile import mkdtemp
from selection import NumericalSelector
from transformation import FillImputer, SimplerImputer, KNNImputerDF
from transformation import OneHotEncoding
from evaluation import get_pareto_front


from sklearn.pipeline import Pipeline
from pipeline import FeatureJoin
import datetime
import time

# Ingnore convergence warnings
from  warnings import simplefilter

from sklearn.exceptions import ConvergenceWarning
simplefilter("ignore", category=ConvergenceWarning)

# Prelude


# Data sets
#datasets = [db.dataset_isbsg]

# Load configuration
FW, DS, DT, AS, PT, LA, EM = Loader().load_config()
datasets = ds_db.get(DS)
data_transformation = dt_db.get(DT)
as_techniques = as_db.get(AS)
pt_techniques = pt_db.get(PT)
ml_techniques = mlt_db.get(LA)

# Mode
# Type of problem to be solved
mode = FW["problem"][0] if "problem" in FW.keys() else "classification"

# Pre processing
# prep = Preprocessing(remove_missing_columns = 0.25, missing_value_handling  = Missing_Value_Handling.MEAN)

prep = Preprocessing( **(FW["preprocessing"] if "preprocessing" in FW.keys() else {}) )

# Baseline and multiobjective
baseline = bl_db[ FW["baseline"][0] if "baseline" in FW.keys() else "none" ]
multiobj = FW["multiobj"]["metrics"] if "multiobj" in FW.keys() and "metrics" in FW["multiobj"].keys() else []
reference = FW["multiobj"]["reference"] if "multiobj" in FW.keys() and "reference" in FW["multiobj"].keys() else []

# Evaluation metrics
eva = Evaluation(EM, baseline, multiobj, reference)

# Cross Validation
# Defaults to 80:20 train test split
cv = cv_db[ FW["cv"][0] if "cv" in FW.keys() else "traintestsplit" ]( **(FW["cv"][1] if "cv" in FW.keys() else {"n_splits":1, "test_size":0.2}) )


# Output dataframe
right_now = datetime.datetime.now()

out_cols = np.append(np.append(["DS", "Iteration", "DP", "AS", "PT", "LA", "PT metric", "Duration (s)"], EM), ["Models built", "Parameters"])
output_df = pd.DataFrame(columns=out_cols)
output_file = "result-" + right_now.strftime('%Y-%m-%d_%H-%M-%S') + ".csv"

# Hyper-parameter output df
output_tuning_df = None
output_tuning_file = "result-hpt-" + right_now.strftime('%Y-%m-%d_%H-%M-%S') + ".csv"

# Pareto-frint output df
output_pareto_df = pd.DataFrame(columns=out_cols)
output_pareto_file = "result-pareto-" + right_now.strftime('%Y-%m-%d_%H-%M-%S') + ".csv"

# Dataset Loop
for ds in datasets:
    ds.set_datapath("data/")
    dataframe = ds.get_dataframe()


    # Data pre-processing
    # dataframe = prep.process(dataframe)
    X = dataframe[ dataframe.columns.difference([ds.predict]) ]
    Y = dataframe[ ds.predict ]
    # Type of problem: classification or regression
    problem = mode if ds.problem == "None" else ds.problem
    
    if type(cv) == LoaderCV:
        cv.set_data( ds.id )
    
    # Cross validation
    for iteration, (train_index, test_index) in enumerate(cv.split(dataframe)):        
        
        X_train, Y_train = X.iloc[train_index,:], Y.iloc[train_index]
        X_test, Y_test = X.iloc[test_index,:], Y.iloc[test_index]
        
        
        # Learning scheme
        # Data Transformation
        for dtt in data_transformation:
            
            # Attribute selection
            for ast in as_techniques:
                astp = ast.parameters
                
                # Learning algorithm
                for mlt in ml_techniques:
                    
                    # Parameter tuning
                    for pst in pt_techniques:
                            current_time = datetime.datetime.now()    
                        
                            print("-"*30)
                            print( current_time.strftime("%d/%m/%Y %H:%M:%S") )
                            print(f"Dataset: {ds.name} ({problem})")
                            print(f"Current iteration: {iteration}")
                            print(f"DT: {dtt.name}")
                            print(f"AS: {ast.name}")
                            print(f"LA: {mlt.name}")
                            print(f"PT: {pst.name}")
                            print(f"Metric: {pst.parameters['scoring'] if 'scoring' in pst.parameters else 'None'}")
                            print("-"*30)
                            
                            # Depending on algorithm
                            # Select set of parameters to evaluate
                            # Tuner acts on the pipeline
                            
                            # Because of pipelines
                            # A new dictionary must be created
                            # Also, separate non-search parameters
                            search_space = {}
                            dt_param = {}
                            as_param = {}
                            ml_param = {}
                            for key, val in dtt.parameters.items():
                                if type(val) == list:
                                    search_space["dt__numerical__transform__" + key] = val
                                else:
                                    dt_param[key] = val
                            for key, val in ast.parameters.items():
                                if type(val) == list:
                                    search_space["as__" + key] = val
                                else:
                                    as_param[key] = val
                            for key, val in mlt.parameters.items():
                                if type(val) == list:
                                    search_space["la__" + key] = val
                                else:
                                    ml_param[key] = val
                            
                            # Finally, train the scheme
                            dttt = dtt.dt_class(**dt_param)
                            
                            model = mlt.get_class(problem)(**ml_param)
                            
                            # if AS is wrapper, use model as estimator
                            if "wrapper" in as_param.keys():
                                if as_param["wrapper"] == True:
                                    as_param["estimator"] = model
                                del as_param["wrapper"]
                                
                            
                            astt = ast.as_class(**as_param)
                            
                            # Create pipeline to select attributes + fit model
                            location = mkdtemp()
                            memory = Memory(location=location, verbose=0)
                            pipe = Pipeline([
                                    ('dt', FeatureJoin(transformer_list=[
                                        ('numerical', Pipeline([
                                                ('select', NumericalSelector(True)),
                                                ('imputation', KNNImputerDF(missing_values = np.nan, n_neighbors=1)),
                                                ('transform', dttt)
                                            ])),
                                        ('categorical', Pipeline([
                                                ('select', NumericalSelector(False)),
                                                ('imputation', FillImputer()),
                                                ('transform', OneHotEncoding(sparse=False, handle_unknown='ignore'))
                                            ]))
                                        ])),
                                    ('as', astt),
                                    ('la', model)
                                     ],memory=memory)
                            
                            # Use requested scoring
                            # We also support multi-objective optimization
                            
                            multiobj_optim = False
                            pt_parameters = pst.parameters.copy()
                            if "scoring" in pt_parameters.keys():
                                met_name = pt_parameters["scoring"]
                                multiobj_optim = type(met_name) == list
                                
                                # We now convert the scoring from name to a function
                                # Or to a dict of functions in the case of multi-objective
                                new_scoring = None
                                
                                if multiobj_optim:
                                    new_scoring = {}
                                    for name in met_name:
                                        new_scoring[name] = make_scorer( eva.get_function(name), greater_is_better = eva.get_greater_is_better(name) )
                                else:
                                    new_scoring = make_scorer( eva.get_function(met_name), greater_is_better = eva.get_greater_is_better(met_name) )
                                
                                pt_parameters["scoring"] = new_scoring
                            
                            # If the scorer is multiobjective
                            # We must define the "main" metric
                            # These will be priorized by tuners
                            if multiobj_optim:
                                # If it is not manually defined
                                # Use the first metric
                                if "refit" not in pt_parameters:
                                    pt_parameters["refit"] = pt_parameters["scoring"].keys[0]
                                else:
                                    # If refit is not on metrics, we add it
                                    refit_name = pt_parameters["refit"]
                                    if refit_name not in pt_parameters["scoring"].keys():
                                        pt_parameters["scoring"][refit_name] = make_scorer( eva.get_function(refit_name), greater_is_better = eva.get_greater_is_better(refit_name) )
                                
                            search = pst.pt_class( pipe, search_space, **pt_parameters )
                            
                            start_time = time.time()
                            
                            search.fit(X_train, Y_train)
                            models_built = len( search.cv_results_["params"] ) * search.n_splits_
                            
                            
                            # If we are using multi-objective, get pareto front
                            # Otherwise, just use the best parameters
                            best_params = []
                            if multiobj_optim:
                                pareto_front = get_pareto_front( search.cv_results_, pst.parameters["scoring"] )
                                best_params = [ search.cv_results_["params"][i] for i in pareto_front ]
                                multiobj_res_df = pd.DataFrame(columns=EM) # Separate dataset for pareto front
                                duration_pareto = 0 # Duration counter
                                models_built_pareto = 0 # Models built counter
                            else:
                                best_params = [ search.best_params_ ]
                            
                            for current_params in best_params:
                                # Re-fit using best parameters
                                pipe.set_params(**current_params)
                                pipe.fit( X_train, Y_train )
                                
                                # Test the model
                                prediction = pipe.predict(X_test)
                                
                                end_time = time.time()
                                duration = end_time - start_time
                                
                                metrics = eva.evaluate(Y_test, prediction)
                                
                                # Output results
                                # Add results to output file
                                scoring = pst.parameters["scoring"] if "scoring" in pst.parameters.keys() else "None"
                                row = [ds.name, iteration, dtt.name, ast.name, pst.name, mlt.name, scoring]
                                row.append( "%.4f" % duration )
                                
                                for metric in metrics.keys():
                                    row.append( "%.4f" % metrics[metric] )
                                
                                row.append( "%d" % models_built )
                                row.append( search.best_params_ )
                                
                                # Save results as file
                                # Each iteration just in case
                                if multiobj_optim:
                                    output_pareto_df = output_pareto_df.append( pd.DataFrame( [row], columns = out_cols ) )
                                    output_pareto_df.to_csv(output_pareto_file, index=False)
                                    duration_pareto += duration
                                    models_built_pareto += models_built
                                    
                                    # Store metrics in another frame to calculate aggregation for front
                                    front_row = []
                                    for metric in metrics.keys():
                                        front_row.append( metrics[metric] )
                                    multiobj_res_df = multiobj_res_df.append( pd.DataFrame( [front_row], columns = EM ) )
                                    
                                else:
                                    output_df = output_df.append( pd.DataFrame( [row], columns = out_cols ) )
                                    output_df.to_csv(output_file, index=False)
                                
                                
                                # Hyper-parameter dataframe
                                hyper_dict = search.cv_results_
                                df_size = len( hyper_dict["params"] )
                                hyper_dict["DS"] = np.repeat(ds.name, df_size)
                                hyper_dict["Iteration"] = np.repeat(iteration, df_size)
                                hyper_dict["DP"] = np.repeat(dtt.name, df_size)
                                hyper_dict["AS"] = np.repeat(ast.name, df_size)
                                hyper_dict["PT"] = np.repeat(pst.name, df_size)
                                hyper_dict["LA"] = np.repeat(mlt.name, df_size)
                                
                                hyper_frame = pd.DataFrame.from_dict(hyper_dict)
                                
                                if output_tuning_df is None:
                                    output_tuning_df = hyper_frame
                                else:
                                    output_tuning_df = pd.concat( [output_tuning_df, hyper_frame] )
                                
                                output_tuning_df.to_csv(output_tuning_file, index=False)
                            
                            # If we are on a pareto front, save average results
                            if multiobj_optim:
                                # Average metrics of the front
                                metrics_front = multiobj_res_df.mean(axis = 0)
                                
                                # Construct row in a format similar to normal frame
                                row = [ds.name, iteration, dtt.name, ast.name, pst.name, mlt.name, scoring]
                                row.append( "%.4f" % duration_pareto )
                                
                                for metric in EM:
                                    row.append( "%.4f" % metrics_front[metric] )
                                
                                row.append( "%d" % models_built )
                                row.append( "pareto front" )
                                
                                # Save to dataframe
                                output_df = output_df.append( pd.DataFrame( [row], columns = out_cols ) )
                                output_df.to_csv(output_file, index=False)
                        
                            # Clear cache
                            rmtree(location)
