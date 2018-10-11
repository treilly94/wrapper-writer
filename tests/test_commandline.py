from argparse import ArgumentTypeError
from unittest import TestCase

from wrapper_writer.commandline import get_args, valid_write_option, existing_files


class TestCommandline(TestCase):

    def test_existing_files(self):
        # Assert raises error when invalid
        for i in ["./tests/cats.txt", "./tests/__init__.py,./tests/cats.txt"]:
            with self.assertRaises(ArgumentTypeError) as cm:
                existing_files(i)
            err = str(cm.exception)
            self.assertEqual("./tests/cats.txt cant be found, does it exist?", err)

        # Assert doesn't raise error when valid
        output = existing_files("./tests/__init__.py")
        self.assertEqual("./tests/__init__.py", output)

    def test_valid_write_option(self):
        # Assert raises error when invalid
        with self.assertRaises(ArgumentTypeError) as cm:
            valid_write_option("pandas")
        err = str(cm.exception)
        self.assertEqual("pandas isn't a valid write option. Must be either w or a", err)

        # Assert doesn't raise error when valid
        for i in ["w", "a"]:
            output = valid_write_option(i)
            self.assertEqual(i, output)

    def test_get_args_wrap(self):
        args_in = ["wrap", "-m", "./tests/__init__.py", "-s", "./tests/test_commandline.py"]
        args_out = get_args(args_in)
        self.assertEqual("wrap", args_out.command)
        self.assertEqual("./tests/__init__.py", args_out.method_config)
        self.assertEqual("./tests/test_commandline.py", args_out.structure_config)

    def test_get_args_parse(self):
        args_in = ["parse", "-c", "./config", "-a", "w", "-f",
                   "./tests/test_commandline.py", "-d", "./tests", "-t", ".*\.py"]
        args_out = get_args(args_in)
        self.assertEqual("parse", args_out.command)
        self.assertEqual("./config", args_out.config_name)
        self.assertEqual("w", args_out.append_config)
        self.assertEqual("./tests/test_commandline.py", args_out.files)
        self.assertEqual("./tests", args_out.directory)
        self.assertEqual(".*\.py", args_out.target_format)
