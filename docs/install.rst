============
Installation
============

The package can be installed in the following ways

From test PyPi Repository
=========================

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
