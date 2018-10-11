from unittest import TestCase

from wrapper_writer.commandline import get_args


class TestCommandline(TestCase):

    def test_get_args(self):
        # Test wrapper
        args_in = ["wrap", "-m", "./tests/__init__.py", "-s", "./tests/test_commandline.py"]
        args_out = get_args(args_in)
        self.assertEqual("wrap", args_out.command)
        self.assertEqual("./tests/__init__.py", args_out.method_config)
        self.assertEqual("./tests/test_commandline.py", args_out.structure_config)
