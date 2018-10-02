from unittest import TestCase
from wrapper_writer.wrapper_writer import WrapperWriter

class TestWrapperWriter(TestCase):
    method_config = "./tests/resources/config/method_config.yml"
    structure_config = "./tests/resources/config/structure_config.yml"

    def test_read_method_config(self):
        w = WrapperWriter()
        w.read_method_config(self.method_config)
        config = w.methods
        expected_config = {
            "sum_column": {
                "params": {"column_a": "String", "column_b": "String",},
                "returns": "String",
                "docs": "This function adds the two columns together"
            },
            "mulitply": {
                "params": {"column_a": "String", "column_b": "String", },
                "returns": "String",
                "docs": "This function multiplies the two columns together"
            }
        }

        self.assertEqual(expected_config, config)

    def test_no_method_in_config(self):
        w = WrapperWriter()
        with self.assertRaises(Exception):
            w.read_method_config(self.structure_config)

    def test_read_structure_config(self):
        w = WrapperWriter()
        w.read_structure_config(self.structure_config)
        config = w.structures
        expected_config = {
            "python": {
                "path": "/test_dir/python/path/",
                "template": "python.txt",
                "file_extension": ".py"
            },
            "scala": {
                "path": "/test_dir/scala/path/",
                "template": "scala.txt",
                "file_extension": ".scala"
            },
        }

        self.assertEqual(expected_config, config)

    def test_no_structure_in_config(self):
        w = WrapperWriter()
        with self.assertRaises(Exception):
            w.read_structure_config(self.method_config)

    # def test_instantiate_structure_class(self):
    #     self.fail()
    #
    # def test_create_directories(self):
    #     self.fail()
    #
    # def test_instantiate_wrapper_class(self):
    #     self.fail()
