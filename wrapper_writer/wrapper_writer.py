import os
import jinja2
import yaml


class WrapperWriter:
    config_dir = ""
    project_root = ""
    method_details = {}

    def __init__(self, config_dir):
        self.config_dir = config_dir

    def create_wrappers(self):
        """This method reads the configuration files and applies them to the project"""
        structure_path = os.path.join(self.config_dir, "directory_structure.yml")
        content = self.read_yaml(structure_path)
        config_path = os.path.join(self.config_dir, "config.yml")
        self.method_details = self.read_yaml(config_path)
        self.project_root = self.get_project_root(content)
        self.create_directories(content)

    def read_yaml(self, path):
        """This method reads  a yaml file into a dictionary"""
        file = open(path)
        config = yaml.load(file)
        file.close()
        return config

    def get_project_root(self, content):
        """This method gets the root from the structure file or sets it to the current working directory"""
        if content.get("project_root") is not None:
            return content.get("project_root")
        else:
            return os.getcwd()

    def create_directories(self, content):
        """This method creates the directory structure defined in the structure file"""
        structure = content.get("directories")
        for part in structure.keys():
            print("Started " + part)
            path = structure[part].get("path")
            full_path = self.project_root + path  # TODO make this use a proper os.path.join
            os.makedirs(full_path)
            self.write_file(full_path, structure, part)
            print("Finished " + part)

    def write_file(self, full_path, structure, part):
        """This method Writes the output from wrapper assembler to a file"""
        output = self.wrapper_assembler(structure[part].get("template"))

        file_name = full_path + self.method_details.get("name") + structure[part].get("file_extension")
        file = open(file_name, "w")
        file.write(output)
        file.close()

    def wrapper_assembler(self, template):
        """This method that assembles the wrapper from a template and the classes method_details"""

        # Get and render the template
        template_dir = os.path.join(self.config_dir, "templates")
        template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template)
        return template.render(method=self.method_details)
