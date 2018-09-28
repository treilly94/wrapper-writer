from unittest import TestCase

from wrapper_writer.container import Container
from wrapper_writer.method import Method


class TestContainer(TestCase):
    m1 = Method("testName",
                {"p1": "String", "p2": "Int"},
                "Test docs",
                "Unit",
                {"Example": "1 + 1 = 2"}
                )
    c_name = "testContainer"
    c_path = "/home/cats/"
    c_methods = [m1]
    container = Container(c_name, c_path, c_methods)

    def test_create_config(self):
        output = self.container.create_config()
        expected = ""

        self.assertEqual(expected, output)
