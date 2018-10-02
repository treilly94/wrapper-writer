import yaml

from wrapper_writer.container import Container
from wrapper_writer.method import Method
from wrapper_writer.structure import Structure
from wrapper_writer.wrapper import Wrapper


class WrapperWriter:
    structures = {}
    containers = {}
    project_root = ""
    structure_classes = []
    container_classes =[]
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
        for i in self.structures.values():
            one_structure = Structure(i.get("path"), i.get("template"), i.get("file_extension"))
            self.structure_classes.append(one_structure)

    def instantiate_container_class(self):
        for i, j in self.containers.items():
            container_methods = []
            print(j)
            for x,v in j.items():
                print(x)
                print("-------------------")
                print(v)
                one_method = Method(x, v.get("params"), v.get("docs"), v.get("returns"), v.get("other"))
                container_methods.append(one_method)
            one_container = Container(i, container_methods)
            self.container_classes.append(one_container)

    def create_directories(self):
        for i in self.structure_classes:
            i.create_path()
            i.create_dir()

    def instantiate_wrapper_class(self):
        for i in self.structure_classes:
            for j in self.container_classes:
                one_wrapper = Wrapper(i.project_root, j, i)
                self.wrappers.append(one_wrapper)


    def run(self):
        self.read_configs()
        self.instantiate_structure_class()
        self.instantiate_container_class()
        self.create_directories()


        self.instantiate_wrapper_class()
        for i in self.wrappers:
            i.write_file()