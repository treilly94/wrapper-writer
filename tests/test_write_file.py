import os
import shutil
from unittest import TestCase

from wrapper_writer.wrapper_writer import WrapperWriter


class TestWriteFile(TestCase):
    method = WrapperWriter("./tests/resources/config/")

    def test_write_file(self):
        self.method.structure = {'python': {'file_extension': '.py',
                                            'path': '/test_dir/',
                                            'template': 'python.txt'}
                                 }
        self.method.methods = {
            "testFunc": {
                "params": {"param1": "String"},
                "returns": "String",
                "docs": None
            }
        }

        path = os.path.join(os.getcwd(), "test_dir")
        os.mkdir(path)

        self.method.write_file(path, "python", "testFunc")

        self.assertTrue(os.path.exists(os.path.join(path, "testFunc.py")))

        # Clean up
        shutil.rmtree('./test_dir/')


def test_file_already_exists(self):
    pass
