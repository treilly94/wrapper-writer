from unittest import TestCase

from wrapper_writer.wrapper_writer import WrapperWriter


class TestWrapperWriter(TestCase):

    method = WrapperWriter("./tests/resources/config/")

    def test_create_wrappers(self):
        self.method.create_wrappers()

    def test_read_config(self):
        output = self.method.read_yaml("./tests/resources/config/config.yml")

        self.assertEqual("testFunc", output["name"])
        self.assertEqual({"param1": "String"}, output["params"])
        self.assertEqual("A cool function", output["docs"])
        self.assertEqual("String", output["returns"])

    def test_wrapper_assembler_python(self):

        self.method.method_details = {
            "name": "testFunc",
            "params": {"param1": "String"},
            "returns": "String",
            "docs": "Test Docs"
        }

        output = self.method.wrapper_assembler("python.txt")

        with open('./tests/resources/expected/python.txt', 'r') as expected_file:
            expected = expected_file.read()

        self.assertEqual(expected, output)

    def test_wrapper_assembler_scala(self):
        self.method.method_details = {
            "name": "testFunc",
            "params": {"param1": "String"},
            "returns": "String",
            "docs": None
        }

        output = self.method.wrapper_assembler("scala.txt")

        with open('./tests/resources/expected/scala.txt', 'r') as expected_file:
            expected = expected_file.read()

        self.assertEqual(expected, output)
