import os

import click
import jinja2
import yaml


class WrapperWriter:
    config_dir = ""
    project_root = ""
    structure = {}
    methods = {}

    def __init__(self, config_dir):
        self.config_dir = config_dir

    def create_wrappers(self):
        """This method reads the configuration files and applies them to the project"""
        config_file_path = os.path.join(self.config_dir, "config.yml")
        self.read_yaml(config_file_path)
        self.create_directories()

    def read_yaml(self, path):
        """This method reads a yaml file into a dictionary"""
        # Read file
        file = open(path)
        config = yaml.load(file)
        file.close()

        # Check if Structure exists
        if "structure" not in config.keys():
            message = "config.yml must contain a structure key"
            raise Exception(message)
        self.structure = config.get("structure")

        # Check if methods exist
        if "methods" not in config.keys():
            message = "config.yml must contain a methods key"
            raise Exception(message)
        self.methods = config.get("methods")

        self.project_root = self.get_project_root(config)

    def get_project_root(self, content):
        """This method gets the root from the structure file or sets it to the current working directory"""
        # Check if project root exists
        if "project_root" not in content.keys():
            message = "config.yml must contain a project_root key, if you wish to use the default please include " \
                      "the key with no value"
            raise Exception(message)
        # Get project root or use default
        if content.get("project_root") is not None:
            return content.get("project_root")
        else:
            return os.getcwd()

    def wrapper_assembler(self, name, template):
        """This name that assembles the wrapper from a template and the classes methods"""
        # Get methods
        method = self.methods[name]
        # Get and render the template
        template_dir = os.path.join(self.config_dir, "templates")
        template_path = os.path.join(template_dir, template)
        # Check template exists
        if not os.path.exists(template_path):
            raise FileNotFoundError

        template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template)
        return template.render(name=name, method=method)

    def write_file(self, full_path, part, method):
        """This method Writes the output from wrapper assembler to a file"""
        file_details = self.structure[part]

        output = self.wrapper_assembler(method, file_details.get("template"))

        file_name = os.path.join(full_path, method + file_details.get("file_extension"))
        file = open(file_name, "w")
        file.write(output)
        file.close()

    def create_directories(self):
        """This method creates the directory structure defined in the structure file"""
        for part in self.structure.keys():
            print("Started " + part)
            # Construct path
            path = self.structure[part].get("path")
            full_path = self.project_root + path  # TODO make this use a proper os.path.join
            # Create path
            try:
                os.makedirs(full_path)
            except FileExistsError:
                print(full_path + " already exists")
            # Create method files
            for method in self.methods:
                self.write_file(full_path, part, method)
            print("Finished " + part)



@click.command()
@click.option("--config_dir", help="The directory containing the config file/templates")
def write_wrappers(config_dir):
    method = WrapperWriter(config_dir)
    method.create_wrappers()


if __name__ == "__main__":
    write_wrappers()
