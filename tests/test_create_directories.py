import os
import shutil
from unittest import TestCase

from wrapper_writer.wrapper_writer import WrapperWriter


class TestCreateDirectories(TestCase):
    method = WrapperWriter("./tests/resources/config/")

    def test_create_directories(self):
        expected_python = os.path.join(os.getcwd(), "test_dir", "python", "path")
        expected_scala = os.path.join(os.getcwd(), "test_dir", "scala", "path")

        self.method.project_root = os.getcwd()
        self.method.structure = {'python': {'path': '/test_dir/python/path/'},
                                 'scala': {'path': '/test_dir/scala/path/'}
                                 }

        self.method.create_directories()

        self.assertTrue(os.path.isdir(expected_python))
        self.assertTrue(os.path.isdir(expected_scala))

        # Clean up
        shutil.rmtree('./test_dir/')

    def test_directories_already_exist(self):
        expected_python = os.path.join(os.getcwd(), "test_dir", "python", "path")
        expected_scala = os.path.join(os.getcwd(), "test_dir", "scala", "path")

        self.method.project_root = os.getcwd()
        self.method.structure = {'python': {'path': '/test_dir/python/path/'},
                                 'scala': {'path': '/test_dir/scala/path/'}
                                 }

        os.makedirs(expected_python)
        os.makedirs(expected_scala)

        try:
            self.method.create_directories()
        except FileExistsError:
            self.fail("create_directories failed because directories already exist")
        finally:
            # Clean up
            shutil.rmtree('./test_dir/')
