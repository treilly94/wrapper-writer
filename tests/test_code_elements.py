from unittest import TestCase

from wrapper_writer.code_elements import Container, Method


class TestContainer(TestCase):

    def setUp(self):
        m1 = Method("testName",
                    {"p1": {"type":"String", "default":"", "doc":""}, "p2": {"type":"Int", "default":"", "doc":""}},
                    "Test docs",
                    "Unit",
                    "public",
                    {"Example": "1 + 1 = 2"}
                    )
        c_name = "testContainer"
        c_path = "/home/cats/"
        c_methods = [m1]
        self.container = Container(c_name, c_methods, c_path)

    def test_format_name(self):
        self.container.format_name()
        self.assertEqual("test_container", self.container.name)

    def test_create_config(self):
        output = self.container.create_config()
        expected = "testContainer:\n" \
                   "  testName:\n" \
                   "    params:\n" \
                   "      p1:\n" \
                   "         type: String\n" \
                   "         default: \n"\
                   "         doc: \"\"\n"\
                   "      p2:\n" \
                   "         type: Int\n" \
                   "         default: \n" \
                   "         doc: \"\"\n" \
                   "    docs: \"Test docs\"\n" \
                   "    returns: Unit\n" \
                   "    access: public\n" \
                   "    other:\n" \
                   "      Example: 1 + 1 = 2\n"

        self.assertEqual(expected, output)


class TestMethod(TestCase):

    def setUp(self):
        name = "testName"
        params = {"paramOne": {"type":"String", "default":"", "doc":"hi"},
                  "ParamTwo": {"type":"Int", "default":"3", "doc":""},
                  "param_three": {"type":"Boolean", "default":True, "doc":""}}
        docs = "Test docs"
        returns = "Unit"
        other = {"Example": "1 + 1 = 2"}

        self.method = Method(name=name, params=params, docs=docs, returns=returns, other=other)

    def test_format_name(self):
        self.method.format_name()
        self.assertEqual("test_name", self.method.name)

    def test_format_params(self):
        self.method.format_params()
        expected = {"param_one": {"type":"String", "default":"", "doc":"hi"},
                    "param_two": {"type":"Int", "default":"3", "doc":""},
                    "param_three": {"type":"Boolean", "default":True, "doc":""}}
        self.assertEqual(expected, self.method.params)
