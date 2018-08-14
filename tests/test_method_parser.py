from unittest import TestCase

from wrapper_writer.method_parser import MethodParser


class TestMethodParser(TestCase):
    def test_scala(self):
        method = """def testFunc(param1: String): String = {
                        param1.toUpperCase
                    }"""

        output = MethodParser()
        output.parse_method(method)

        self.assertEqual(output.name, "testFunc")
        self.assertEqual(output.params, [("param1", "String")])
        self.assertEqual(output.docs, "")
        self.assertEqual(output.returns, "String")

    def test_read_config(self):
        output = MethodParser()
        output.read_from_config()

        self.assertEqual(output.name, "testFunc")
        self.assertEqual(output.params, [("param1", "String")])
        self.assertEqual(output.docs, "")
        self.assertEqual(output.returns, "String")
