import os
import shutil
from unittest import TestCase

from wrapper_writer.container import Container
from wrapper_writer.method import Method
from wrapper_writer.structure import Structure
from wrapper_writer.wrapper import Wrapper


# This test must be run with the working directory set as the project root
class TestWrapper(TestCase):
    def setUp(self):
        m1 = Method(name="test_func",
                    params={"param1": "String"},
                    returns="String",
                    docs="A cool function",
                    other={})

        container = Container(name="test_container", path="", methods=[m1])
        structure = Structure(path="./test_dir", template="testTemplate.scala.j2", file_name_format="prefix_%s.txt")
        self.wrapper = Wrapper(project_root="./tests/resources/config/", container=container, structure=structure)

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
        expected = "./test_dir/prefix_test_container.txt"
        output = self.wrapper.create_file_name()

        self.assertEqual(expected, output)

    def test_write_file(self):
        try:
            path = os.path.join(os.getcwd(), "test_dir")
            os.mkdir(path)

            self.wrapper.write_file()

            self.assertTrue(os.path.exists(os.path.join(path, "prefix_test_container.txt")))

        # Clean up
        finally:
            shutil.rmtree('./test_dir/')
