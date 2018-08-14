import jinja2


def wrapper_assembler(templates_dir, template, method):
    """A method that assembles the wrapper from a method object and a wrapper config"""

    # Get and render the template
    template_loader = jinja2.FileSystemLoader(searchpath=templates_dir)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template)
    return template.render(method=method)
