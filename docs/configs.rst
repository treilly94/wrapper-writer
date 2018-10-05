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

