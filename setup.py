from setuptools import setup, find_packages

setup(
    name='wrapper_writer',
    version='0.3',
    author="Tom Reilly",
    url="https://github.com/treilly94/wrapper-writer",
    packages=find_packages(),
    install_requires=[
        "Jinja2",
        "MarkupSafe",
        "PyYAML"
    ],
    entry_points='''
        [console_scripts]
        wrapper_writer=wrapper_writer.commandline:commandline
    ''',
)
