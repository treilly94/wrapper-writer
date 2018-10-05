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

