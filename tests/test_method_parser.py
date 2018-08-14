from unittest import TestCase

from wrapper_writer.method_parser import MethodParser


class TestMethodParser(TestCase):
    def test_scala(self):
        method = """def testFunc(param1: String): String = {
                        param1.toUpperCase
                    }"""

        output = MethodParser(method)
        output.parse_method()

        self.assertEqual(output.name, "testFunc")
        self.assertEqual(output.params, [("param1", "String")])
        self.assertEqual(output.docs, "")
        self.assertEqual(output.returns, "String")
