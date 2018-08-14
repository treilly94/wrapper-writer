from unittest import TestCase

from wrapper_writer.method_parser import MethodParser
from wrapper_writer.wrapper_assembler import wrapper_assembler


class TestWrapperAssembler(TestCase):
    method = MethodParser()
    method.name = "testFunc"
    method.params = [("param1", "String")]
    method.returns = "String"
    method.docs = ""

    def test_python_wrapper(self):
        output = wrapper_assembler("python.txt", self.method)

        with open('./tests/resources/wrapper_assembler/python.txt', 'r') as expected_file:
            expected = expected_file.read()

        self.assertEqual(output, expected)

    # def test_java_api_wrapper(self):
    #     output = wrapper_assembler("java.txt", self.method)
    #
    #     with open('./tests/resources/java_api_wrapper.txt', 'r') as expected_file:
    #         expected = expected_file.read()
    #
    #     self.assertEqual(output, expected)
