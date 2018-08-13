import re


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
        pattern = r'def (\w+)\((.*)\): (\w+)'
        searched = re.search(pattern, self.method)
        self.method_name = searched.group(1)
        self.method_params = self.parse_params(searched.group(2))
        self.method_returns = searched.group(3)

    @staticmethod
    def parse_params(params):
        """This method splits the parameters and places them in the correct format"""
        new_params = []
        # Remove whitespace and split parameters by a comma
        params = params.replace(" ", "").split(",")

        for p in params:
            p = p.split(":")
            new_params.append((p[0], p[1]))

        return new_params
