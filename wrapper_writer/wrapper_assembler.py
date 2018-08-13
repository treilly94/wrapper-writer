import jinja2


def wrapper_assembler(method):
    """A method that assembles the wrapper from a method object and a wrapper config"""

    # Get and render the template
    template_loader = jinja2.FileSystemLoader(searchpath="./templates/")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("python.txt")
    return template.render(name=method.method_name, params=method.method_params)
