def get_problem_type(problem):
    """
    Function:
        get_problem_type
    Description:
        Safely returns a string as one of 4 problem times: regression, classification, both or none
    Input:
        - problem,str: Type of problem.
    Output:
        String representing type of problem, and none if not in the 4 types
    """
    if problem.lower() in ["regression", "classification", "both", "none"]:
        return problem.lower()
    else:
        return "none"