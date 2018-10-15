import os
import shutil
import sys
from unittest import TestCase

from wrapper_writer.code_elements import Container, Method
from wrapper_writer.structure import Structure
from wrapper_writer.wrapper import Wrapper


# This test must be run with the working directory set as the project root
class TestWrapper(TestCase):
    def setUp(self):
        self.m1 = Method(name="test_func",
                         params={"param1": "String"},
                         returns="String",
                         docs="A cool function",
                         access="public",
                         other={})

        container = Container(name="test_container", path="", methods=[self.m1])
        structure = Structure(project_root=os.getcwd(), path="./test_dir", template="testTemplate.scala.j2",
                              access=["public", "protected"], file_name_format="prefix_{}.txt")
        self.wrapper = Wrapper(project_root="./tests/resources/", container=container, structure=structure)

    def test_filter_access(self):
        # Add new test functions
        m2 = Method(name="test_func2",
                    params={"param1": "String"},
                    returns="String",
                    docs="A cool function",
                    access="private",
                    other={})
        m3 = Method(name="test_func3",
                    params={"param1": "String"},
                    returns="String",
                    docs="A cool function",
                    access="protected",
                    other={})

        self.wrapper.container.methods.extend([m2, m3])

        # Call method
        self.wrapper.filter_access()

        # Assert
        self.assertListEqual([self.m1, m3], self.wrapper.container.methods)

    def test_populate_template(self):
        output = self.wrapper.populate_template()

        with open('./tests/resources/expected/testContainer.scala', 'r') as expected_file:
            expected = expected_file.read()

        self.assertEqual(expected, output)

    def test_populate_template_no_template(self):
        self.wrapper.structure.template = "cats.txt"
        with self.assertRaises(FileNotFoundError):
            self.wrapper.populate_template()

    def test_create_file_name(self):
        self.wrapper.structure.full_path = "./test_dir"
        if sys.platform.startswith("win"):
            expected = "./test_dir\prefix_test_container.txt"
        else:
            expected = "./test_dir/prefix_test_container.txt"
        output = self.wrapper.create_file_name()

        self.assertEqual(expected, output)

    def test_write_file(self):
        try:
            path = os.path.join(os.getcwd(), "test_dir")
            os.mkdir(path)
            self.wrapper.structure.full_path = "./test_dir"
            self.wrapper.write_file()

            self.assertTrue(os.path.exists(os.path.join(path, "prefix_test_container.txt")))

        # Clean up
        finally:
            shutil.rmtree('./test_dir/')
