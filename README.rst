.. image:: https://travis-ci.org/treilly94/wrapper-writer.svg?branch=master
    :target: https://travis-ci.org/treilly94/wrapper-writer

.. image:: https://img.shields.io/badge/taiga-kanban-green.svg
    :target: https://tree.taiga.io/project/treilly94-wrapper-writer/

==============
wrapper-writer
==============

This package dynamically creates wrappers for your methods in a given structure


============
Installation
============

The package can be installed in the following ways

From the test PyPi Repository
=============================

Use the below command to install the latest published version from the test pypi repository.

.. warning::
    This may fail if the dependencies are not already installed as many of them are not available from the test pypi
    repo.

.. code-block:: bash

    pip3 install --index-url https://test.pypi.org/simple/ wrapper_writer

From Source
===========

The following command can be run in the same folder as the setup.py to install the package from a local copy of the
code.

.. code-block:: bash

    pip3 install --editable .


=====================
Commandline Interface
=====================

Once installed the Wrapper Writer module can be called from the command line using the below command

.. code-block:: bash

    wrapper_writer

This takes the following arguments:

-h, --help  Describe the command and its arguments/subcommands.

Wrap
====

Wrap is a subcommand that will call the wrapper functionality. The below example will run the wrap functionality with
default values

.. code-block:: bash

    wrapper_writer wrap


This takes the following arguments:

-h, --help              Describe the subcommand and its arguments.
-m, --method-config     The path to the method config file.
                        default='./method_config.yml
-s, --structure-config  The path to the structure config file.
                        default='./structure_config.yml

.. note::
    The wrapper requires both the method and structure configs.

Parse
=====

The parse functionality is currently in development. The below example will print out "Parsing ..."

.. code-block:: bash

    wrapper_writer parse


This takes the following arguments:

-h, --help  Describe the subcommand and its arguments.


===================
Configuration Files
===================

There are currently two configuration files. They are both written in yaml syntax.


Structure Config
================

The default name of this file is **structure_config.yml** and it is expected to be in the cwd, although this can be
changed by passing arguments at runtime.

The structure config defines the following details of the project:

**project_root**
    The root of the project being worked on. If left blank this will default to the cwd.

It also contains the following details of each type of wrapper:

**path**
    The location to put the generated files relative to the project root

**template**
    The name of the template to use for these wrappers.

**file_name_format**
    The format of the name of the generated files. This is a string that will be formatted.
    A **{}** symbol will represent the container name. The container name can be converted into Upper or Lower camelcase by
    placing either **!u** or **!l** inside **{}**.

Below is an example of the structure config.

.. code-block:: yaml

    # The absolute path of the root of the target project
    # If none is provided your cwd will be used
    project_root:

    # The structure of the project
    # All paths are relative to the project_root
    structure:
      api:
        path: src/main/scala/com/example/api/
        template: api.scala.j2
        file_name_format: "{!u}API.scala"
      impl:
        path: src/main/scala/com/example/implicits/
        template: implicits.scala.j2
        file_name_format: "{!u}Impl.scala"
      python:
        path: python/methods/
        template: python.py.j2
        file_name_format: "{}.py"
      r:
        path: R/R/
        template: r.R.j2
        file_name_format: "sdf_{}.R"


Methods Config
==============

The default name of this file is **method_config.yml** and it is expected to be in the cwd, although this can be
changed by passing arguments at runtime.

The methods config file contains details of the methods to be wrapped. Below is a example of the structure:

.. code-block:: yaml

    container_name: # The name of the file/class/object that contains the methods
        method_name: # The name of the method to be wrapped
            params: # A dictionary of the methods parameters and their types
                param1: type1
                param2: type2
            docs: # The methods documentation
            returns: # The return type of the method
            other: # Other is for any optional extra information that the user wants in the templates
                other1: additional thing 1

.. warning::
    It is recommended that all method and container names are written in lowercase with words separated by underscores.
    If they aren't the functionality to convert them in to different cases may not work.

The below example shows three methods spread between two containers

.. code-block:: yaml

    maths:
      sum_columns:
        params:
          df: DataFrame
          column_a: String
          column_b: String
          new_col: String
        docs: This function takes in a DataFrame and then adds a new column to it which holds the values of columnA + columnB. This is calculated by calling the sumColumns function when adding the new column.
        returns: DataFrame
      multiply:
        params:
          df: DataFrame
          column_a: String
          column_b: String
          new_col: String
        docs: This function takes in two integers and multiplies them together and return the outcome.
        returns: DataFrame

    operations:
      filter_on_list:
        params:
          df: DataFrame
          target_col: String
          values: List[Int]
        docs: This function calls a protected function which filters the data based on where the targetCol doesn't have values that are in the values parameter.
        returns: DataFrame


=========
Templates
=========

The templates are written in the `Jinja2 <http://jinja.pocoo.org/docs/2.10/>`_ syntax and are expected in the templates
directory in the project root.

Examples of the templates can be found in the examples folder of this project.

Containers
==========
The container object will be made available within the templates. It will contain the following variables:

**name**
    The name of the container

**path**
    The path of the container if it was parsed

**methods**
    This is a list of all the method objects associated with the container.

Methods
=======
The Method objects can be found in the methods list in the container object as described above. They will contain the
following variables:

**name**
    The name of the method

**params**
    A dictionary of the parameters where the keys are the names and the values are the types.

**docs**
    The methods documentation

**returns**
    The methods return type

**other**
    A user defined object. It can be whatever you need. Just add it into the method config.

Filters
=======

Custom filters have been added into the jinja environment so that strings with underscores between the words can be
converted into Upper or Lower camelcase. An example of the syntax is below.

.. code-block:: Jinja

    {{ container.name|upper_camel }}
    {{ container.name|lower_camel }}


==============
Scala Parser
==============

This module parses a scala file and create method config to use for Wrapper Writer


