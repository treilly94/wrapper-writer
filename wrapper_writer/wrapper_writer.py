import yaml

from wrapper_writer.structure import Structure
from wrapper_writer.wrapper import Wrapper


class WrapperWriter:
    structures = {}
    containers = {}
    project_root = ""
    structure_classes = []
    wrappers = []

    def __init__(self, method_config_path="./configs/method_config.yml",
                 structure_config_path="./configs/structure_config.yml"):
        self.method_config_path = method_config_path
        self.structure_config_path = structure_config_path

    def read_configs(self):
        """This method reads a yaml file into a dictionary"""
        # Read file
        file = open(self.method_config_path)
        self.containers = yaml.load(file)
        file.close()

        # Read file
        file = open(self.structure_config_path)
        config = yaml.load(file)
        file.close()

        # Check if Structure exists
        if "structure" not in config.keys():
            message = "config.yml must contain a structure key"
            raise Exception(message)
        self.structures = config.get("structure")
        self.project_root = config.get("project_root")

    def instantiate_structure_class(self):
        for i in self.structures:
            struct = self.structures.get(i)
            one_structure = Structure(struct.get("path"), struct.get("template"), struct.get("file_extension"))
            self.structure_classes.append(one_structure)

    def create_directories(self):
        for i in self.structure_classes:
            i.create_path()
            i.create_dir()

    def instantiate_wrapper_class(self):
        for i in self.structure_classes:
            for j in self.containers:
                container = self.containers.get(j)
                one_wrapper = Wrapper(i.project_root, container, i)
                self.wrappers.append(one_wrapper)


    def run(self):
        self.instantiate_structure_class()