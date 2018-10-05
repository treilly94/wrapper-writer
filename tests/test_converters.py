from unittest import TestCase

from wrapper_writer.converters import lower_camel, upper_camel


class TestConverters(TestCase):
    def test_lower_camel_default(self):
        out = lower_camel("test_func_one")
        self.assertEqual("testFuncOne", out)

    def test_lower_camel_other(self):
        out = lower_camel("test.func.one", ".")
        self.assertEqual("testFuncOne", out)

    def test_upper_camel_default(self):
        out = upper_camel("test_func_one")
        self.assertEqual("TestFuncOne", out)

    def test_upper_camel_other(self):
        out = upper_camel("test.func.one", ".")
        self.assertEqual("TestFuncOne", out)
