from unittest import TestCase

from wrapper_writer.container import Container
from wrapper_writer.method import Method
from wrapper_writer.structure import Structure
from wrapper_writer.wrapper import Wrapper


# This test must be run with the working directory set as the project root
class TestWrapper(TestCase):
    m1 = Method(name="test_func",
                params={"param1": "String"},
                returns="String",
                docs="A cool function",
                other={})

    container = Container(name="test_container", path="", methods=[m1])
    structure = Structure(path="", template="testTemplate.scala.j2", file_name_format="")
    wrapper = Wrapper(project_root="./tests/resources/config/", container=container, structure=structure)

    def test_populate_template(self):
        output = self.wrapper.populate_template()

        with open('./tests/resources/expected/testContainer.scala', 'r') as expected_file:
            expected = expected_file.read()

        self.assertEqual(expected, output)

    def test_create_file_name(self):
        self.fail()

    def test_write_file(self):
        self.fail()
