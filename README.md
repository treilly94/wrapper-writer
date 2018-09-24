[![Build Status](https://travis-ci.org/treilly94/wrapper-writer.svg?branch=development)](https://travis-ci.org/treilly94/wrapper-writer)
[![](https://img.shields.io/badge/taiga-kanban-green.svg)](https://tree.taiga.io/project/treilly94-wrapper-writer/)
# wrapper-writer
This package dynamically creates wrappers for your methods in a given structure

## Instillation 
The package can be installed in the following ways
#### From test pypi
Use the below command to install from test pypi.  
This may fail if the dependencies are not already installed as many of them are not available from the test pypi repo. 
```
pip3 install --index-url https://test.pypi.org/simple/ wrapper_writer 
```
#### From a local copy
The following command can be run in the same folder as the setup.py to install the package from a local copy of the 
code.
```
pip3 install --editable .
```

## Config file
The config file is written in yaml and should be named *config.yml*.  
It should contain the following details:
### Project root
This variable must either be the absolute path of the root of your target project or left blank. If left blank your 
current working directory will be used as the project root.
### Structure
This is a dictionary that describes the various paths within the project and what sort of files they should contain  
Each directory should have:
* A memorable name
* The relative path to the directory
* The template to use
* The file extension to use  

Each directory will be created if it doesnt already exist 
### Methods
This is a dictionary that contains the details of the methods to be used in the templates. It can contain whatever 
variables the user requires. These will be translated into a python dictionary and made
available in the templates

### Example
```yaml
# The absolute path of the root of the target project
# If none is provided your cwd will be used
project_root:

# The structure of the project
# All paths are relative to the project_root
structure:
  python:
    path: /test_dir/python/path/
    template: python.txt
    file_extension: .py
  scala:
    path: /test_dir/scala/path/
    template: scala.txt
    file_extension: .scala

# The details of the methods to be templated
methods:
  testFunc:
    params:
      param1: String
    docs: A cool function
    returns: String
```

## Templates
The templates are made using the [Jinja2](http://jinja.pocoo.org) syntax.
### Name
They can be named anything but must be located in a folder called *templates* in the same directory as the 
config file.
#### Accessing variables from the method config
The variables from the method config will be available in the template through a python dictionary called *method*, 
and the method name will be made available through a name variable.

### Example
```python
# This block sets variables from within the method object for more easy calling
{%- set params = method.get("params") -%}
{%- set docs = method.get("docs") -%}
def {{ name }}({% for p in params.keys() %}{{ p }}{% endfor %}):
    {% if docs != None -%}
    """ {{ docs }}"""
    {%- endif %}

    api = jvm.TestFunc

    DataFrame(api.{{ name }}({% for p in params.keys() %}{{ p }}{% endfor %}), sql_ctx)
``` 

## Running the package
Once the package has been installed it can be run by calling *wrapper_writer*  
It takes the following parameters:  
--config_dir = The directory containing the config file

So running the function from the config directory would look like 
```bash
wrapper_writer --config_dir .
```
