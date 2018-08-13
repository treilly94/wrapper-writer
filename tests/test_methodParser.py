from unittest import TestCase

from wrapper_writer.method_parser import MethodParser


class TestMethodParser(TestCase):
    def test_scala(self):
        method = """def testFunc(param1: String): String = {
                        param1.toUpperCase
                    }"""

        output = MethodParser(method)

        self.assertEqual(output.method_name, "testFunc")
        self.assertEqual(output.method_params, [("param1", "String")])
        self.assertEqual(output.method_docs, "")
        self.assertEqual(output.method_returns, "String")
