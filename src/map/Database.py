class Database():
    
    def __init__(self, classtype, mapping = {}, base_params = {}):
        self.classtype = classtype
        self.mapping = mapping
        self.base_params = base_params
    
    def get(self, items):
        res = []
        for item in items:
            x = self.get_one(item)
            if x is not None:
                res.append(x)
        return res
    
    def get_one(self, item):
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
