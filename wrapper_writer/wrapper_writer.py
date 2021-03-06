import os

import yaml

from wrapper_writer.code_elements import Container, Method
from wrapper_writer.structure import Structure
from wrapper_writer.wrapper import Wrapper


class WrapperWriter:
    """
    The WrapperWriter class contains the details and functionality associated writing a wrapper file based on two
    configs.

    :param method_config_path: The path to the method config file relative to the cwd.
    :type method_config_path: str
    :param structure_config_path: The path to the structure config file relative to the cwd.
    :type structure_config_path: str
    """
    structures = {}  #: The dictionary which holds all the information from the structure config.
    containers = {}  #: The dictionary which holds all the information from the methods config.
    project_root = ""  #: The absolute path to the current working directory.
    structure_classes = []  #: The list which holds all the structure classes.
    container_classes = []  #: The list which holds all the container classes.
    wrappers = []  #: The list which holds all the wrapper classes.

    def __init__(self, method_config_path="./method_config.yml",
                 structure_config_path="./structure_config.yml"):
        self.method_config_path = os.path.normpath(method_config_path)
        self.structure_config_path = os.path.normpath(structure_config_path)

    def default_string(self):
        """
        This function makes sure that the string defaults are inputted into the dictionary as '"fred"'
        This is to ensure that the are printed correctly when they are wrapped.
        """
        for i, j in self.containers.items():
            for x, v in j.items():
                for t, l in v.get("params").items():
                    if l.get("type") == "String" and l.get("default") is not None:
                        l["default"] = '"' + l.get("default") + '"'

    def read_configs(self):
        """
        This function will read in two yml files and saved them as two dictionaries, containers and structures. It will
        then get the project root from the structures yml file.
        """

        # Read methods
        file = open(self.method_config_path)
        self.containers = yaml.load(file)
        self.default_string()
        file.close()

        # Read Structure
        file = open(self.structure_config_path)
        structure_config = yaml.load(file)
        file.close()

        # Check if Structure exists
        if "structure" not in structure_config.keys():
            message = "the structure config must contain a structure key"
            raise Exception(message)
        self.structures = structure_config.get("structure")
        if structure_config.get("project_root"):
            self.project_root = os.path.normpath(structure_config.get("project_root"))
        else:
            self.project_root = os.getcwd()

    def instantiate_structure_class(self):
        """
        This function will instantiate the Structure class for each structure within the structures dictionary class
        parameter. It will store in class within a list.
        """
        for i in self.structures.values():
            one_structure = Structure(project_root=self.project_root,
                                      path=i.get("path"),
                                      template=i.get("template"),
                                      access=i.get("access", "public"),
                                      file_name_format=i.get("file_name_format"))
            self.structure_classes.append(one_structure)

    def instantiate_container_class(self):
        """
        This function will instantiate the Container class for each container within the container dictionary class
        parameter. It will store in class within a list.
        """
        for i, j in self.containers.items():
            container_methods = []
            for x, v in j.items():
                print(v.get("params"))
                one_method = Method(name=x,
                                    params=v.get("params"),
                                    docs=v.get("docs"),
                                    returns=v.get("returns"),
                                    access=v.get("access", "public"),
                                    other=v.get("other"))
                container_methods.append(one_method)
            one_container = Container(i, container_methods)
            self.container_classes.append(one_container)

    def create_directories(self):
        """
        This function will take the structure_classes parameter and called the create_path and create_dir functions
        for each structure class within the list.
        """
        for i in self.structure_classes:
            i.create_path()
            i.create_dir()

    def instantiate_wrapper_class(self):
        """
        This function will instantiate the Wrapper class for each structure and each container within the
        structure and container class. It will store these wrapper classes within a list.
        """
        for i in self.structure_classes:
            for j in self.container_classes:
                one_wrapper = Wrapper(self.project_root, j, i)
                self.wrappers.append(one_wrapper)

    def run(self):
        """
        This function will run the above method in order to produce a wrapper file.
        """
        self.read_configs()
        self.instantiate_structure_class()
        self.instantiate_container_class()
        self.create_directories()

        self.instantiate_wrapper_class()
        for i in self.wrappers:
            i.filter_access()
            i.write_file()
