def get_metrics_problem(metrics, problem):
    """
        Function:
            get_metrics_problem
        Description:
            From a list of Metrics, returns only those that match with problem.
        Input:
            - metrics,list: List of Metric objects
            - problem,str: Type of problem
        Output:
            List of metric objects that match problem
    """
    return [ e for e in metrics if e.problem == problem ]

def evaluate(y, y_pred, metrics, problem):
    """
        Function:
            evaluate
        Description:
            Evaluate all the metrics for a list of predicted values.
            For a given problem type.
        Input:
            - y,list: List of the true y values
            - y_pred,list: List of predicted y values
            - metrics,list: List of Metric objects
            - problem,str: Type of problem
        Output:
            List of metric objects that match problem
    """
    return dict( [(m.name, m.evaluate(y, y_pred)) for m in get_metrics_problem(metrics, problem)] )

def get_all_scorers( metrics, problem ):
    """
        Function:
            get_all_scorers
        Description:
            Return the scorer of all metrics of a certain problem type.
        Input:
            - metrics,list: List of Metric objects
            - problem,str: Type of problem
        Output:
            Dictonary of format { name : scorer }
    """
    return dict( [(m.name, m.make_scorer()) for m in get_metrics_problem(metrics, problem)] )

def get_metrics_by_name(metrics, names):
    """
        Function:
            get_metrics_by_name
        Description:
            Return metrics that match the selected names.
        Input:
            - metrics,list: List of Metric objects
            - names,list: List of metric names
        Output:
            List of metric objects that match names
    """
    return [ m for m in metrics if m.name in names ]

def get_metricx_list(type, features):
    """
        Function:
            get_metricx_list
        Description:
            Return an instance of a MetricX for each feature name on a list.
        Input:
            - type,class: The MetricX object to instance.
            - features,list: List of feature names.
        Output:
            Dictionary of MetricX objects, one per feature.
    """
    return dict([ (f"{type().name}-{f}" , type(f) ) for f in features ])
