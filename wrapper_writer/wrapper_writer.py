import yaml

from wrapper_writer.structure import Structure


class WrapperWriter:
    structures = {}
    methods = {}
    project_root = ""


    def read_method_config(self, path):
        """This method reads a yaml file into a dictionary"""
        # Read file
        file = open(path)
        config = yaml.load(file)
        file.close()

        # Check if methods exist
        if "methods" not in config.keys():
            message = "config.yml must contain a methods key"
            raise Exception(message)
        self.methods = config.get("methods")

    def read_structure_config(self, path):
        # Read file
        file = open(path)
        config = yaml.load(file)
        file.close()

        # Check if Structure exists
        if "structure" not in config.keys():
            message = "config.yml must contain a structure key"
            raise Exception(message)
        self.structures = config.get("structure")
        self.project_root = config.get("project_root")

    def instantiate_structure_class(self, path, template, file_name_format):
        self.structure_class = Structure(path, template, file_name_format)

    def create_directories(self):
        for i in self.structures:
            self.structure_class = Structure(i.path, i.template, i.file_name_format)
            self.structure_class.create_path()
            self.structure_class.create_dir()

    def instantiate_wrapper_class(self):
        self.wrapper_class = WrapperWriter()