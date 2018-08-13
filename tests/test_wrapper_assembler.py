from unittest import TestCase

from wrapper_writer.method_parser import MethodParser
from wrapper_writer.wrapper_assembler import wrapper_assembler


class TestWrapperAssembler(TestCase):
    method = MethodParser("")
    method.method_name = "testFunc"
    method.method_params = [("param1", "String")]
    method.method_returns = "String"
    method.method_docs = ""

    def test_python_wrapper(self):
        output = wrapper_assembler(self.method)

        expected = """def test_func(param1):
                        api = jvm.TestFunc
                        
                        DataFrame(api.testFunc(param1), sql_ctx)"""

        self.assertEqual(output, expected)
