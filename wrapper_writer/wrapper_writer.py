import os
import jinja2
import yaml


class WrapperWriter:
    config_dir = ""
    method_details = {}

    def __init__(self, config_dir):
        self.config_dir = config_dir

    def create_wrappers(self, config_dir):
        """This method reads the configuration files and applies them to the project"""
        # Read structure

        # Create directory if it doesnt

    def read_yaml(self, path):
        """This method reads  a yaml file into a dictionary"""
        file = open(path)
        config = yaml.load(file)
        file.close()
        return config

    def wrapper_assembler(self, template):
        """This method that assembles the wrapper from a template and the classes method_details"""

        # Get and render the template
        template_dir = os.path.join(self.config_dir, "templates")
        template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template)
        return template.render(method=self.method_details)
