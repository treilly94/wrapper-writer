import re


class MethodParser:
    """A class that parses the details of each method"""

    name = ""
    params = ""
    docs = ""
    returns = ""

    def read_from_config(self):
        """This method reads the details of the method from a config file"""

    def parse_method(self, method):
        """This method parses the target method as a string into its individual components"""
        pattern = r'def (\w+)\((.*)\): (\w+)'
        searched = re.search(pattern, method)
        self.name = searched.group(1)
        self.params = self.parse_params(searched.group(2))
        self.returns = searched.group(3)

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
