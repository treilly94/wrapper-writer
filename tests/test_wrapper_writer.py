import os
import shutil
from unittest import TestCase

from wrapper_writer.code_elements import Container, Method
from wrapper_writer.structure import Structure
from wrapper_writer.wrapper_writer import WrapperWriter


class TestWrapperWriter(TestCase):
    method_config = "./tests/resources/config/method_config.yml"
    structure_config = "./tests/resources/config/structure_config.yml"
    project_root = os.getcwd()

    container = {
        "Maths": {
            "sum_column": {
                "params": {"column_a": {'default': None, 'doc': 'Name of column to add.', 'type': 'String'},
                           "column_b": {'default': None, 'doc': 'Name of column to add.', 'type': 'String'}},
                "returns": "String",
                "docs": "This function adds the two columns together"
            },
            "mulitply": {
                "params": {"column_a": {'default': None, 'doc': 'Name of column to multiply.', 'type': 'String'},
                           "column_b": {'default': None, 'doc': 'Name of column to multiply.', 'type': 'String'}},
                "returns": "String",
                "docs": "This function multiplies the two columns together"
            }
        },
        "Estimation": {"ratio": {
            "params": {"column_a": {'default': '"numbers"', 'doc': 'Name of column to estimate.', 'type': 'String'},
                       "column_b": {'default': None, 'doc': '', 'type': 'String'}},
            "returns": "String",
            "docs": "This function does ratio estimation"
        }}
    }
    structure = {
        "python": {
            "path": "/test_dir/python/path/",
            "template": "python.txt",
            "file_name_format": "{}.py"
        },
        "scala": {
            "path": "/test_dir/scala/path/",
            "template": "scala.txt",
            "file_name_format": "{}.scala"
        },
    }

    structure_class = [Structure(project_root, "./test_dir/python/path/", "python.txt", ".py"),
                       Structure(project_root, "./test_dir/scala/path/", "scala.txt", ".scala")]

    def test_read_method_configs(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.read_configs()
        config = w.containers

        self.assertEqual(self.container, config)

    def test_read_structure_config(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.read_configs()
        config = w.structures

        self.assertEqual(self.structure, config)

    def test_no_structure_in_config(self):
        w = WrapperWriter(self.method_config, self.method_config)
        with self.assertRaises(Exception) as cm:
            w.read_configs()
        err = str(cm.exception)
        self.assertEqual("the structure config must contain a structure key", err)

    def test_instantiate_structure_class(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.structures = self.structure
        w.instantiate_structure_class()
        self.assertEqual(os.path.normpath("/test_dir/python/path"), w.structure_classes[0].path)
        self.assertEqual("python.txt", w.structure_classes[0].template)
        self.assertEqual("{}.py", w.structure_classes[0].file_name_format)

        self.assertEqual(os.path.normpath("/test_dir/scala/path"), w.structure_classes[1].path)
        self.assertEqual("scala.txt", w.structure_classes[1].template)
        self.assertEqual("{}.scala", w.structure_classes[1].file_name_format)

    def test_instantiate_container_class(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.containers = self.container
        w.instantiate_container_class()

        self.assertEqual("Maths", w.container_classes[0].name)
        self.assertEqual("sum_column", w.container_classes[0].methods[0].name)
        self.assertEqual({"column_a": {'default': None, 'doc': 'Name of column to add.', 'type': 'String'},
                          "column_b": {'default': None, 'doc': 'Name of column to add.', 'type': 'String'}},
                         w.container_classes[0].methods[0].params)
        self.assertEqual("This function adds the two columns together", w.container_classes[0].methods[0].docs)
        self.assertEqual("String", w.container_classes[0].methods[0].returns)

        self.assertEqual("mulitply", w.container_classes[0].methods[1].name)
        self.assertEqual({"column_a": {'default': None, 'doc': 'Name of column to multiply.', 'type': 'String'},
                          "column_b": {'default': None, 'doc': 'Name of column to multiply.', 'type': 'String'}},
                         w.container_classes[0].methods[1].params)
        self.assertEqual("This function multiplies the two columns together", w.container_classes[0].methods[1].docs)
        self.assertEqual("String", w.container_classes[0].methods[1].returns)

        self.assertEqual("Estimation", w.container_classes[1].name)
        self.assertEqual("ratio", w.container_classes[1].methods[0].name)
        self.assertEqual({"column_a": {'default': '"numbers"', 'doc': 'Name of column to estimate.', 'type': 'String'},
                          "column_b": {'default': None, 'doc': '', 'type': 'String'}},
                         w.container_classes[1].methods[0].params)
        self.assertEqual("This function does ratio estimation", w.container_classes[1].methods[0].docs)
        self.assertEqual("String", w.container_classes[1].methods[0].returns)

    def test_create_directories(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.structure_classes = self.structure_class

        try:
            w.create_directories()

            self.assertTrue(os.path.isdir(os.path.join(os.getcwd(), "./test_dir/python/path/")))
            self.assertTrue(os.path.isdir(os.path.join(os.getcwd(), "./test_dir/scala/path/")))
        finally:
            shutil.rmtree("./test_dir/")

    def test_instantiate_wrapper_class(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.project_root = self.project_root
        w.structure_classes = self.structure_class
        w.container_classes = [Container("Maths",
                                         [Method("sum_column", {"column_a": "String", "column_b": "String"},
                                                 "This function adds the two columns together", "String", None),
                                          Method("mulitply", {"column_a": "String", "column_b": "String"},
                                                 "This function multiplies the two columns together", "String", None)
                                          ]),
                               Container("Estimation", [Method("ratio", {"column_a": "String", "column_b": "String"},
                                                               "This function does ratio estimation", "String", None)])
                               ]

        w.instantiate_wrapper_class()
        self.assertEqual(self.project_root, w.wrappers[0].project_root)

        self.assertEqual("Maths", w.wrappers[0].container.name)
        self.assertEqual("sum_column", w.wrappers[0].container.methods[0].name)
        self.assertEqual({"column_a": "String", "column_b": "String"}, w.wrappers[0].container.methods[0].params)
        self.assertEqual("This function adds the two columns together", w.wrappers[0].container.methods[0].docs)
        self.assertEqual("String", w.wrappers[0].container.methods[0].returns)
        self.assertEqual("mulitply", w.wrappers[0].container.methods[1].name)
        self.assertEqual({"column_a": "String", "column_b": "String"}, w.wrappers[0].container.methods[1].params)
        self.assertEqual("This function multiplies the two columns together", w.wrappers[0].container.methods[1].docs)
        self.assertEqual("String", w.wrappers[0].container.methods[1].returns)

        self.assertEqual(os.path.normpath("test_dir/python/path"), w.wrappers[0].structure.path)
        self.assertEqual("python.txt", w.wrappers[0].structure.template)
        self.assertEqual(".py", w.wrappers[0].structure.file_name_format)

        self.assertEqual("Estimation", w.wrappers[1].container.name)
        self.assertEqual("ratio", w.wrappers[1].container.methods[0].name)
        self.assertEqual({"column_a": "String", "column_b": "String"}, w.wrappers[1].container.methods[0].params)
        self.assertEqual("This function does ratio estimation", w.wrappers[1].container.methods[0].docs)
        self.assertEqual("String", w.wrappers[1].container.methods[0].returns)

        self.assertEqual(os.path.normpath("test_dir/python/path"), w.wrappers[1].structure.path)
        self.assertEqual("python.txt", w.wrappers[1].structure.template)
        self.assertEqual(".py", w.wrappers[1].structure.file_name_format)

        self.assertEqual("Maths", w.wrappers[2].container.name)
        self.assertEqual("sum_column", w.wrappers[2].container.methods[0].name)
        self.assertEqual({"column_a": "String", "column_b": "String"}, w.wrappers[2].container.methods[0].params)
        self.assertEqual("This function adds the two columns together", w.wrappers[2].container.methods[0].docs)
        self.assertEqual("String", w.wrappers[2].container.methods[0].returns)
        self.assertEqual("mulitply", w.wrappers[2].container.methods[1].name)
        self.assertEqual({"column_a": "String", "column_b": "String"}, w.wrappers[2].container.methods[1].params)
        self.assertEqual("This function multiplies the two columns together",
                         w.wrappers[2].container.methods[1].docs)
        self.assertEqual("String", w.wrappers[2].container.methods[1].returns)

        self.assertEqual(os.path.normpath("test_dir/scala/path"), w.wrappers[2].structure.path)
        self.assertEqual("scala.txt", w.wrappers[2].structure.template)
        self.assertEqual(".scala", w.wrappers[2].structure.file_name_format)

        self.assertEqual("Estimation", w.wrappers[3].container.name)
        self.assertEqual("ratio", w.wrappers[3].container.methods[0].name)
        self.assertEqual({"column_a": "String", "column_b": "String"}, w.wrappers[3].container.methods[0].params)
        self.assertEqual("This function does ratio estimation", w.wrappers[3].container.methods[0].docs)
        self.assertEqual("String", w.wrappers[3].container.methods[0].returns)

        self.assertEqual(os.path.normpath("test_dir/scala/path"), w.wrappers[3].structure.path)
        self.assertEqual("scala.txt", w.wrappers[3].structure.template)
        self.assertEqual(".scala", w.wrappers[3].structure.file_name_format)

    def test_default_string(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.containers = {
            "Maths": {
                "sum_column": {
                    "params": {"column_a": {'default': "fred", 'doc': 'Name of column to add.', 'type': 'String'}},
                    "returns": "String",
                    "docs": "This function adds the two columns together"
                }}}
        w.default_string()

        self.assertEqual('"fred"',
                         w.containers.get("Maths").get("sum_column").get("params").get("column_a").get("default"))

    def test_default_string_nodefault(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.containers = {
            "Maths": {
                "sum_column": {
                    "params": {"column_a": {'default': None, 'doc': 'Name of column to add.', 'type': 'String'}},
                    "returns": "String",
                    "docs": "This function adds the two columns together"
                }}}
        w.default_string()

        self.assertEqual(None, w.containers.get("Maths").get("sum_column").get("params").get("column_a").get("default"))

    def test_default_string_int_default(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.containers = {
            "Maths": {
                "sum_column": {
                    "params": {"column_a": {'default': '2', 'doc': 'Name of column to add.', 'type': 'Int'}},
                    "returns": "String",
                    "docs": "This function adds the two columns together"
                }}}
        w.default_string()

        self.assertEqual('2', w.containers.get("Maths").get("sum_column").get("params").get("column_a").get("default"))

    def test_default_string_list_String(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.containers = {
            "Maths": {
                "sum_column": {
                    "params": {"column_a": {'default': 'List["fred"]', 'doc': 'Name of column to add.',
                                            'type': 'List[String]'}},
                    "returns": "String",
                    "docs": "This function adds the two columns together"
                }}}
        w.default_string()

        self.assertEqual('List["fred"]',
                         w.containers.get("Maths").get("sum_column").get("params").get("column_a").get("default"))

    def test_default_string_multiple(self):
        w = WrapperWriter(self.method_config, self.structure_config)
        w.containers = {
            "Maths": {
                "sum_column": {
                    "params": {"column_a": {'default': 'List["fred"]', 'doc': 'Name of column to add.',
                                            'type': 'List[String]'},
                               "column_b": {'default': 'fred', 'doc': 'Name of column to add.', 'type': 'String'}},
                    "returns": "String",
                    "docs": "This function adds the two columns together"
                }}}
        w.default_string()

        self.assertEqual('List["fred"]',
                         w.containers.get("Maths").get("sum_column").get("params").get("column_a").get("default"))
        self.assertEqual('"fred"',
                         w.containers.get("Maths").get("sum_column").get("params").get("column_b").get("default"))
