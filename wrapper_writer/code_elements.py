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
            config += "    docs: \"%s\"\n" % m.docs
            # Method returns
            config += "    returns: %s\n" % m.returns
            # Method access
            config += "    access: %s\n" % m.access
            # Method other
            config += "    other:\n"
            for k, v in m.other.items():
                config += "      %s: %s\n" % (k, v)

        return config


class Method:
    """The Method Class contains the details associated with a particular method.

    :param name: The name of the method.
    :type name: str
    :param params: A dictionary where the keys are the methods parameter names and the values are the types.
    :type params: dict
    :param docs: The docstring of the method.
    :type docs: str
    :param returns: The return type of the object.
    :type returns: str
    :param access: The access modifier of the method e.g. public, private.
    :type access: str
    :param other: A dictionary containing any additional values that may be required in the template.
    :type other: dict
    """

    def __init__(self, name, params, docs, returns, access="public", other={}):

        self.name = name
        self.params = params
        self.docs = docs
        self.returns = returns
        self.access = access.lower()
        self.other = other
