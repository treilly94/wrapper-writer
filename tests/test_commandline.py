from unittest import TestCase

from wrapper_writer.commandline import get_args


class TestCommandline(TestCase):

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
