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
default values:

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

The parse subcommand will create the methods_config file from one or more scala files, or a directory containing one
or more scala files. The below example will run the parse functionality on two given files and a directory:

.. code-block:: bash

    wrapper_writer parse -f /path/to/file/one.scala,/path/to/file/two.scala -d /path/to/dir/


This takes the following arguments:

-h, --help  Describe the subcommand and its arguments.
-c, --config-name  The name of the config file to write to
-a, --append-config  a: Append an existing config file, w: Overwrite if config file exists
-f, --files  A comma separated list of absolute file paths to be parsed
-d, --directory  The absolute path to a directory containing files to be parsed
-t, --target-format  The format of the files to read from the directory