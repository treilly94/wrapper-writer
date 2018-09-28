class Container:
    def __init__(self, name, path, methods):
        self.name = name
        self.path = path
        self.methods = methods

    def create_config(self):
        """This method formats the details of the container and its methods into a yml syntax"""
        # Set container name
        config = "%s:\n" % self.name
        # Loop through methods
        for m in self.methods:
            # Method name
            config += "\t%s:\n" % m.name
            # Method params
            config += "\t\tparams:\n"
            for k, v in m.params.items():
                config += "\t\t\t%s: %s\n" % (k, v)
            # Method docs
            config += "\t\tdocs: %s\n" % m.docs
            # Method returns
            config += "\t\treturns: %s\n" % m.returns
            # Method other
            config += "\t\tother:\n"
            for k, v in m.other.items():
                config += "\t\t\t%s: %s\n" % (k, v)

        return config
