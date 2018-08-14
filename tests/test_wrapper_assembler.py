from unittest import TestCase

from wrapper_writer.wrapper_assembler import WrapperWriter


class TestWrapperWriter(TestCase):

    method = WrapperWriter("./tests/resources/templates/")

    def test_read_config(self):
        self.method.read_from_config("./tests/resources/configs/config.yml")
        output = self.method.config

        self.assertEqual("testFunc", output["name"])
        self.assertEqual({"param1": "String"}, output["params"])
        self.assertEqual(None, output["docs"])
        self.assertEqual("String", output["returns"])

    def test_wrapper_assembler_python(self):

        self.method.config = {
            "name": "testFunc",
            "params": {"param1": "String"},
            "returns": "String",
            "docs": None
        }

        output = self.method.wrapper_assembler("python.txt")

        with open('./tests/resources/expected/python.txt', 'r') as expected_file:
            expected = expected_file.read()

        self.assertEqual(expected, output)

    def test_wrapper_assembler_scala(self):
        self.method.config = {
            "name": "testFunc",
            "params": {"param1": "String"},
            "returns": "String",
            "docs": None
        }

        output = self.method.wrapper_assembler("scala.txt")

        with open('./tests/resources/expected/scala.txt', 'r') as expected_file:
            expected = expected_file.read()

        self.assertEqual(expected, output)
