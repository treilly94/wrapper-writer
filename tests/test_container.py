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
    container = Container(c_name, c_methods, c_path)

    def test_create_config(self):
        output = self.container.create_config()
        expected = "testContainer:\n" \
                   "\ttestName:\n" \
                   "\t\tparams:\n" \
                   "\t\t\tp1: String\n" \
                   "\t\t\tp2: Int\n" \
                   "\t\tdocs: Test docs\n" \
                   "\t\treturns: Unit\n" \
                   "\t\tother:\n" \
                   "\t\t\tExample: 1 + 1 = 2\n"

        self.assertEqual(expected, output)
