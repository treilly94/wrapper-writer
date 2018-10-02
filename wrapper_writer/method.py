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
    :param other: A dictionary containing any additional values that may be required in the template.
    :type other: dict
    """

    def __init__(self, name, params, docs, returns, other):

        self.name = name
        self.params = params
        self.docs = docs
        self.returns = returns
        self.other = other
