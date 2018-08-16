from unittest import TestCase

from wrapper_writer.wrapper_writer import WrapperWriter


class TestWriteFile(TestCase):
    method = WrapperWriter("./tests/resources/config/")

    def test_write_file(self):
        pass