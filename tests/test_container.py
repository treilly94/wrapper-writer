from unittest import TestCase

from wrapper_writer.method_containers import Container, Method


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
                   "  testName:\n" \
                   "    params:\n" \
                   "      p1: String\n" \
                   "      p2: Int\n" \
                   "    docs: \"Test docs\"\n" \
                   "    returns: Unit\n" \
                   "    other:\n" \
                   "      Example: 1 + 1 = 2\n"

        self.assertEqual(expected, output)
