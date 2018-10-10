class Container:
    """The Container Class contains the details and functionality associated with a particular container.

    .. note:: A container is any entity that contains one or more methods. e.g. a class, a object, or a file

    :param name: The name of the container.
    :type name: str
    :param path: The path of the container relative to the project root.
    :type path: str
    :param methods: The methods associated with the container.
    :type methods: list
    """
    def __init__(self, name, methods, path=None):
        self.name = name
        self.path = path
        self.methods = methods

    def create_config(self):
        """This method formats the details of the container and its methods into a yml syntax

        :return: str
        """
        # Set container name
        config = "%s:\n" % self.name
        # Loop through methods
        for m in self.methods:
            # Method name
            config += "  %s:\n" % m.name
            # Method params
            config += "    params:\n"
            for k, v in m.params.items():
                config += "      %s: %s\n" % (k, v)
            # Method docs
            config += "    docs: %s\n" % m.docs
            # Method returns
            config += "    returns: %s\n" % m.returns
            # Method other
            config += "    other:\n"
            for k, v in m.other.items():
                config += "      %s: %s\n" % (k, v)

        return config
