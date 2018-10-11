from argparse import Namespace

from unittest import TestCase

from wrapper_writer.commandline import wrap


class TestCommandline(TestCase):

    def test_wrap(self):
        # Check invalid method_config
        with self.assertRaises(Exception) as cm:
            args = Namespace
            args.method_config = "./test.yml"
            args.structure_config = "./test.yml"
            wrap(args)
        err = str(cm.exception)
        self.assertEqual("[Errno 2] No such file or directory: 'test.yml'", err)
