import os

import jinja2

from wrapper_writer.converters import upper_camel, lower_camel


class Wrapper:
    """The Wrapper Class contains the details and functionality associated with a particular wrapper.

    :param project_root: The root of the project the wrappers will be written to.
    :type project_root: str
    :param container: The container associated with the wrapper.
    :type container: Container
    :param structure: The method associated with the wrapper.
    :type structure: Structure
    """

    def __init__(self, project_root, container, structure):
        self.project_root = project_root
        self.container = container
        self.structure = structure

    def populate_template(self):
        """This method populates the template defined in the structure with the details of the container.

        :return: str
        """
        # Get the template path
        template_dir = os.path.join(self.project_root, "templates")
        template_path = os.path.join(template_dir, self.structure.template)

        # Check template exists
        if not os.path.exists(template_path):
            raise FileNotFoundError

        # Create the jinja2 environment
        template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
        template_env = jinja2.Environment(loader=template_loader)

        # Add the converters to the jinja2 environment
        template_env.filters["lower_camel"] = lower_camel
        template_env.filters["upper_camel"] = upper_camel

        # Render the template
        template = template_env.get_template(self.structure.template)

        return template.render(container=self.container)

    def create_file_name(self):
        """This method formats the file name and adds it to the end of the path defined in the structure.

        :return: str
        """
        # Format filename

        filename = self.structure.file_name_format.format(self.container.name)

        # Add path
        return os.path.join(self.structure.full_path, filename)

    def write_file(self):
        """This method populates the template, creates the appropriate file name, and writes the file.

        :return: None
        """
        # Get completed template
        output = self.populate_template()

        # Get file name
        file_name = self.create_file_name()

        # Write file
        file = open(file_name, "w")
        file.write(output)
        file.close()
