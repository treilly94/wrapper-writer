[![Build Status](https://travis-ci.org/treilly94/wrapper-writer.svg?branch=development)](https://travis-ci.org/treilly94/wrapper-writer)
[![](https://img.shields.io/badge/taiga-kanban-green.svg)](https://tree.taiga.io/project/treilly94-wrapper-writer/)
# wrapper-writer
This package dynamically creates wrappers for your methods in a given structure

## Method config
Currently the details of the method are defined in a yaml file. 
#### Name
The yaml file must be called *config.yml* and must be in the same directory as the structure file.  
#### Content
The file can contain whatever variables the user requires. These will be translated into a python dictionary and made
available in the templates

## Structure config
Currently the details of the project structure are contained in a yaml file.
#### Name
This file must be called *directory_structure.yml* and must be located in the same directory ast the method config file.
#### Content
This file must contain the following information.  
##### project_root
This variable must either be the absolute path of the root of your target project or left blank. If left blank your 
current working directory will be used as the project root.
##### directories 
These variables specify the details of the directories.  
They must have:  
* A memorable name
* The relative path to the directory
* The template to use
* The file extension to use  

Each directory will be created if it doesnt already exist 

A example of the file can be seen below 
```yaml
project_root:

directories:
  python:
    path: /test_dir/python/path/
    template: python.txt
    file_extension: .py
  scala:
    path: /test_dir/scala/path/
    template: scala.txt
    file_extension: .scala
```

## Wrapper templates
The wrapper templates are made using the [Jinja2](http://jinja.pocoo.org) syntax.
#### Name
They can be named anything but must be located in a folder called *templates* in the same directory as the 
method config, and structure files.
#### Accessing variables from the method config
The variables from the method config will be available in the template through a python dictionary called *method*.

An example of a python template can be seen below
```python
# This block sets variables from within the method object for more easy calling
{%- set name = method.get("name") -%}
{%- set params = method.get("params") -%}
{%- set docs = method.get("docs") -%}

def {{ name }}({% for p in params.keys() %}{{ p }}{% endfor %}):
    {% if docs != None -%}
    """ {{ docs }}"""
    {%- endif %}

    api = jvm.TestFunc

    DataFrame(api.{{ name }}({% for p in params.keys() %}{{ p }}{% endfor %}), sql_ctx)
``` 