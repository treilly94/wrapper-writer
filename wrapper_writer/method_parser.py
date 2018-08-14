import re
import yaml


class MethodParser:
    """A class that parses the details of each method"""

    name = ""
    params = ""
    docs = ""
    returns = ""

    def read_from_config(self, config):
        """This method reads the details of the method from a yaml config file"""
        config_dict = yaml.load(open(config))

        self.name = config_dict.get("name")
        self.params = config_dict.get("params")
        self.docs = config_dict.get("docs")
        self.returns = config_dict.get("returns")


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
