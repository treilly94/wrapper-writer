import os
from unittest import TestCase

from wrapper_writer.wrapper_writer import WrapperWriter


class TestGetProjectRoot(TestCase):
    method = WrapperWriter("./tests/resources/config/")

    def test_get_project_root(self):
        content = {"project_root": "/home/test"}

        output = self.method.get_project_root(content)

        self.assertEqual("/home/test", output)

    def test_default_project_root(self):
        content = {"project_root": None}

        output = self.method.get_project_root(content)

        cwd = os.getcwd()

        self.assertEqual(cwd, output)

    def test_null_project_root(self):
        content = {}

        with self.assertRaises(Exception) as cm:
            self.method.get_project_root(content)
        err = str(cm.exception)
        message = "config.yml must contain a project_root key, if you wish to use the default please include " \
                  "the key with no value"
        self.assertEqual(message, err)
