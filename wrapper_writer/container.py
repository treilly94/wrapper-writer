class Container:
    def __init__(self, name, path, methods):
        self.name = name
        self.path = path
        self.methods = methods

    def create_config(self):
        """This method formats the details of the container and its methods into a yml syntax"""
        config = "%s:\n" % self.name
        for m in self.methods:
            config += "\t%s:\n" % m.name
            config += "\t\tparams:\n"
            for k, v in m.params.items():
                config += "\t\t\t%s: %s\n" % (k, v)
            config += "\t\tdocs: %s\n" % m.docs
            config += "\t\treturns: %s\n" % m.returns
            config += "\t\tother:\n"
            for k, v in m.other.items():
                config += "\t\t\t%s: %s\n" % (k, v)

        return config
