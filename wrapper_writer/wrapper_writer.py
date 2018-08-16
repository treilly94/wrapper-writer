import os
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
        """This method reads  a yaml file into a dictionary"""
        file = open(path)
        config = yaml.load(file)
        file.close()
        self.structure = config.get("structure")
        self.methods = config.get("methods")
        self.project_root = self.get_project_root(config)

    def get_project_root(self, content):
        """This method gets the root from the structure file or sets it to the current working directory"""
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
            path = self.structure[part].get("path")
            full_path = self.project_root + path  # TODO make this use a proper os.path.join
            os.makedirs(full_path)
            for method in self.methods:
                self.write_file(full_path, part, method)
            print("Finished " + part)
