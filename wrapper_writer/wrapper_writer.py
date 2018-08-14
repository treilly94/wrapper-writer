import os
import jinja2
import yaml


class WrapperWriter:
    config_dir = ""
    method_details = {}

    def __init__(self, config_dir):
        self.config_dir = config_dir

    # def create_wrappers(self, config_dir):

    def read_from_config(self, config):
        """This method reads the details of the method from a yaml method_details file"""
        file = open(config)
        self.method_details = yaml.load(file)
        file.close()

    def wrapper_assembler(self, template):
        """A method that assembles the wrapper from a method object and a wrapper method_details"""

        # Get and render the template
        template_dir = os.path.join(self.config_dir, "templates")
        template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template)
        return template.render(method=self.method_details)
