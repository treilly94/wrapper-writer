===========
Basic Usage
===========

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