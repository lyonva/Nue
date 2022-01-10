import numpy as np

def get_pareto_front(cv_results, metrics):
    cv_names = [ "mean_test_" + metric.name for metric in metrics ]
    cv_metrics = [ cv_results[ name ] for name in cv_names ]
    pareto_front = []
    
    # Now, search for the pareto front
    # 1) No solution in the front is strictly better than any other
    # 2) Solutions that are strictly worse are removed
    
    # We do this process for each explored hyper-parameter
    for i in range(len( cv_metrics[0] )):
        included = True # We start assuming the current parameter can be included
        
        # Now, check for each of the pareto-front
        # Whether it is overshadowed by any other parameter
        for fp in pareto_front:
            overshadowed = True # Assume it is, until we find a case it isnt
            
            # Check for each metric
            for m_object, metric in zip(metrics, cv_metrics):
                # Gets around Nan values
                if True in np.isnan(metric): break
                
                sign = m_object._sign # Metric sign
                
                # Check if metric is overshadowed
                overshadowed = overshadowed and ( metric[fp] * sign >= metric[i] * sign )
                if not overshadowed: break # If we found it is not, stop searching
            
            # If the parameter is overshadowed by someone in the front, it is not included
            included = included and not(overshadowed)
            if not included: break # End if we already found it its not included
        
        # If the metric was not overshadowed by anyone, its a new point
        # Now, find out if the new point overshadows some of the existing points
        if included:            
            for fp in pareto_front:
                overshadowed = True # Assume it is, until we find a case it isnt
                
                # Check for each metric
                for m_object, metric in zip(metrics, cv_metrics):
                    sign = m_object._sign # Metric sign
                    
                    # Check if metric is overshadowed
                    overshadowed = overshadowed and ( metric[i] * sign >= metric[fp] * sign )
                    if not overshadowed: break # If we found it is not, stop searching
                
                # If it is overshadowed by the new point, remove
                if overshadowed: pareto_front.remove(fp)
            
            # Lastly, add the new point to the front
            pareto_front.append(i)
    
    return pareto_front
