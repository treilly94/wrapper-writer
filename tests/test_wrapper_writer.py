from unittest import TestCase

import os

import shutil

from wrapper_writer.structure import Structure
from wrapper_writer.wrapper_writer import WrapperWriter


class TestWrapperWriter(TestCase):
    method_config = "./tests/resources/config/method_config.yml"
    structure_config = "./tests/resources/config/structure_config.yml"

    def test_read_configs(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.read_configs()
        config = w.containers
        expected_config = {
            "Maths": {
                "sum_column": {
                    "params": {"column_a": "String", "column_b": "String", },
                    "returns": "String",
                    "docs": "This function adds the two columns together"
                },
                "mulitply": {
                    "params": {"column_a": "String", "column_b": "String", },
                    "returns": "String",
                    "docs": "This function multiplies the two columns together"
                }
            },
            "Estimation": {"ratio": {
                "params": {"column_a": "String", "column_b": "String", },
                "returns": "String",
                "docs": "This function does ratio estimation"
            }}
        }

        self.assertEqual(expected_config, config)

    def test_read_structure_config(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.read_configs()
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
        w = WrapperWriter(self.method_config, self.method_config)
        with self.assertRaises(Exception):
            w.read_configs()

    def test_instantiate_structure_class(self):
        w = WrapperWriter(self.method_config, self.method_config)
        w.structures = {
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
        w.instantiate_structure_class()
        self.assertEquals("/test_dir/python/path/", w.structure_classes[0].path)
        self.assertEquals("python.txt", w.structure_classes[0].template)
        self.assertEquals(".py", w.structure_classes[0].file_name_format)

        self.assertEquals("/test_dir/scala/path/", w.structure_classes[1].path)
        self.assertEquals("scala.txt", w.structure_classes[1].template)
        self.assertEquals(".scala", w.structure_classes[1].file_name_format)


    def test_create_directories(self):
        w = WrapperWriter(self.method_config, self.method_config)
        w.structure_classes = [Structure("./test_dir/python/path/", "python.txt", ".py"),
                               Structure("./test_dir/scala/path/", "scala.txt", ".scala")]
        w.create_directories()

        self.assertTrue(os.path.isdir(os.path.join(os.getcwd(), "./test_dir/python/path/")))
        self.assertTrue(os.path.isdir(os.path.join(os.getcwd(), "./test_dir/scala/path/")))

        shutil.rmtree("./test_dir/")

    # def test_instantiate_wrapper_class(self):
    #     self.fail()
