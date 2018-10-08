from setuptools import setup, find_packages

setup(
    name='wrapper_writer',
    version='0.4',
    author="Tom Reilly, Kayleigh Bellis, Ian Edward",
    url="https://github.com/treilly94/wrapper-writer",
    description=('Wrapper Writer aims to make the creation of repetitive files '
                 'easier using templates and simple configuration files.'),
    license='MIT',
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
