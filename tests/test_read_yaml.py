from unittest import TestCase

from wrapper_writer.wrapper_writer import WrapperWriter


class TestReadYaml(TestCase):
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

    def test_no_file(self):
        with self.assertRaises(FileNotFoundError):
            self.method.read_yaml("./tests/resources/config/no_file.yml")

    def test_no_structure(self):
        with self.assertRaises(Exception) as cm:
            self.method.read_yaml("./tests/resources/config/no_structure.yml")
        err = str(cm.exception)
        self.assertEqual("config.yml must contain a structure key", err)

    def test_no_methods(self):
        with self.assertRaises(Exception) as cm:
            self.method.read_yaml("./tests/resources/config/no_methods.yml")
        err = str(cm.exception)
        self.assertEqual("config.yml must contain a methods key", err)
