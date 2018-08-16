import shutil
from unittest import TestCase

from wrapper_writer.wrapper_writer import WrapperWriter


class TestWrapperWriter(TestCase):
    method = WrapperWriter("./tests/resources/config/")

    def test_read_yaml(self):
        self.method.read_yaml("./tests/resources/config/config.yml")
        expected_structure = {'python': {'file_extension': '.py',
                                         'path': '/test_dir/python/path/',
                                         'template': 'python.txt'},
                              'scala': {'file_extension': '.scala',
                                        'path': '/test_dir/scala/path/',
                                        'template': 'scala.txt'}
                              }
        expected_methods = {'testFunc': {'docs': 'A cool function',
                                         'params': {'param1': 'String'},
                                         'returns': 'String'}
                            }

        self.assertEqual(expected_structure, self.method.structure)
        self.assertEqual(expected_methods, self.method.methods)

    def test_get_project_root(self):
        pass

    def test_wrapper_assembler_python(self):
        self.method.methods = {
            "testFunc": {
                "params": {"param1": "String"},
                "returns": "String",
                "docs": "A cool function"
            }
        }

        output = self.method.wrapper_assembler("testFunc", "python.txt")

        with open('./tests/resources/expected/python.txt', 'r') as expected_file:
            expected = expected_file.read()

        self.assertEqual(expected, output)

    def test_wrapper_assembler_scala(self):
        self.method.methods = {
            "name": "testFunc",
            "params": {"param1": "String"},
            "returns": "String",
            "docs": None
        }

        output = self.method.wrapper_assembler("testFunc", "scala.txt")

        with open('./tests/resources/expected/scala_without_docs.txt', 'r') as expected_file:
            expected = expected_file.read()

        self.assertEqual(expected, output)

    def test_write_files(self):
        pass

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
