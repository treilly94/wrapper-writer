from unittest import TestCase

from wrapper_writer.method_containers import Method


class TestMethod(TestCase):

    def test_method(self):
        name = "testName"
        params = {"p1": "String", "p2": "Int"}
        docs = "Test docs"
        returns = "Unit"
        other = {"Example": "1 + 1 = 2"}

        m = Method(name=name, params=params, docs=docs, returns=returns, other=other)

        self.assertEqual(name, m.name)
        self.assertEqual(params, m.params)
        self.assertEqual(docs, m.docs)
        self.assertEqual(returns, m.returns)
        self.assertEqual(other, m.other)
