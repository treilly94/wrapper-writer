import jinja2
import yaml


class WrapperWriter:
    templates_dir = ""
    config = {}

    def __init__(self, templates_dir):
        self.templates_dir = templates_dir

    def read_from_config(self, config):
        """This method reads the details of the method from a yaml config file"""
        file = open(config)
        self.config = yaml.load(file)
        file.close()

    def wrapper_assembler(self, template):
        """A method that assembles the wrapper from a method object and a wrapper config"""

        # Get and render the template
        template_loader = jinja2.FileSystemLoader(searchpath=self.templates_dir)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template)
        return template.render(method=self.config)
