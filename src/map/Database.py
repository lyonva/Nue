class Database():
    """
    Class:
        Database
    Description:
        Storage for parts of the machine learning process.
        Each database represents one technique type.
        e.x.: Data transformations, parameter optimizers.
        Used to convert names into appropriate classes.
        Values are returned as container class "classtype".
    """
    def __init__(self, classtype, mapping = {}, base_params = {}):
        """
        Function:
            __init__
        Description:
            Returns an instance of Database.
        Input:
            - classtype,class: Container class, all returned items are of this type.
            - mapping,dict: mapping of name into one class
            - base_params: mapping of name into default parameters
        Output:
            List of instances of container class.
            Size is at most equal to input list.
            If a certain name is not found, nothing is included.
        """
        self.classtype = classtype
        self.mapping = mapping
        self.base_params = base_params
    
    def get(self, items):
        """
        Function:
            get
        Description:
            Returns a list of container classes, if applicable.
            If items are not matched, returns whatever it can.
        Input:
            - items,list: Pairs of (name, params) values
        Output:
            List of instances of container class.
            Size is at most equal to input list.
            If a certain name is not found, nothing is included.
        """
        res = []
        for item in items:
            x = self.get_one(item)
            if x is not None:
                res.append(x)
        return res
    
    def get_one(self, item):
        """
        Function:
            get_one
        Description:
            Gets container class and hyper params.
            From a name and (user defined) hyper parameters of a method.
            User-defined parameters are given priority.
        Input:
            - name,str: name of the technique.
            - parameters,dict: user defined hyper parameters.
        Output:
            Instance of the container class.
        """
        try:
            name, params = item
            if name.lower() in self.base_params.keys():
                base = self.base_params[name].copy()
            else:
                base = {}
            for k in params:
                base[k] = params[k]
            return self.classtype( name, self.mapping[name.lower()], base )
        except:
            return None


class DatabaseTwoClass(Database):
    """
    Class:
        DatabaseTwoClass
    Description:
        Extends Database to store objects that have to possible classes.
        e.x. Learners (classification and regression).
    """

    def get_one(self, item):
        """
        Function:
            get_one
        Description:
            Gets container class and hyper params.
            From a name and (user defined) hyper parameters of a method.
            User-defined parameters are given priority
        Input:
            - name,str: name of the technique.
            - parameters,dict: user defined hyper parameters.
        Output:
            Instance of the container class.
        """
        try:
            name, params = item
            if name.lower() in self.base_params.keys():
                base = self.base_params[name].copy()
            else:
                base = {}
            for k in params:
                base[k] = params[k]
            return self.classtype( name, self.mapping[name.lower()][0],\
                    self.mapping[name.lower()][1], base )
        except:
            return None
