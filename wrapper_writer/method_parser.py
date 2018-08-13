class MethodParser:
    """A class that parses the details of each method"""

    method_name = ""
    method_params = ""
    method_docs = ""
    method_returns = ""

    def __init__(self, method_string):
        self.method = method_string
        self.parse_method()

    def parse_method(self):
        """This method parses the target method as a string into its individual components"""
