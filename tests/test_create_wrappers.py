import shutil
from unittest import TestCase

from wrapper_writer.wrapper_writer import WrapperWriter


class TestCreateWrappers(TestCase):
    method = WrapperWriter("./tests/resources/config/")

    def test_create_wrappers(self):
        self.method.create_wrappers()

        # Check Python
        with open('./tests/resources/expected/python.txt', 'r') as expected_file:
            expected = expected_file.read()

        with open('./test_dir/python/path/testFunc.py', 'r') as output_file:
            output = output_file.read()

        self.assertEqual(expected, output)

        # Check Scala
        with open('./tests/resources/expected/scala_with_docs.txt', 'r') as expected_file:
            expected = expected_file.read()

        with open('./test_dir/scala/path/testFunc.scala', 'r') as output_file:
            output = output_file.read()

        self.assertEqual(expected, output)

        # Clean up
        shutil.rmtree('./test_dir/')
