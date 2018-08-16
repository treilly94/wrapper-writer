from unittest import TestCase

from wrapper_writer.wrapper_writer import WrapperWriter


class TestWrapperAssembler(TestCase):
    method = WrapperWriter("./tests/resources/config/")

    def test_wrapper_assembler_simple_docs(self):
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

    def test_wrapper_assembler_no_docs(self):
        self.method.methods = {
            "testFunc": {
                "params": {"param1": "String"},
                "returns": "String",
                "docs": None
            }
        }

        output = self.method.wrapper_assembler("testFunc", "scala.txt")

        with open('./tests/resources/expected/scala_without_docs.txt', 'r') as expected_file:
            expected = expected_file.read()

        self.assertEqual(expected, output)

    def test_wrapper_assembler_no_template(self):
        with self.assertRaises(FileNotFoundError):
            self.method.wrapper_assembler("testFunc", "C.txt")
