import os
import shutil
from unittest import TestCase

from wrapper_writer.structure import Structure


class TestStructure(TestCase):
    path = "./tests/dir/tests"
    template = ""
    file_name_format = ""
    project_root = ""

    def test_create_path(self):
        absolute_path = os.path.normpath(os.path.join(os.getcwd(), self.path))

        # Calling the structure class
        s = Structure(os.getcwd(), self.path, self.template, self.file_name_format)
        s.create_path()
        full_path = s.full_path

        self.assertEqual(absolute_path, full_path)

    def test_create_dir(self):
        absolute_path = os.path.join(os.getcwd(), self.path)

        # Calling the structure class
        s = Structure(self.project_root, self.path, self.template, self.file_name_format)
        s.full_path = absolute_path
        try:
            s.create_dir()
            self.assertTrue(os.path.isdir(absolute_path))
        finally:
            shutil.rmtree("./tests/" + self.path.split("/")[2])

    def test_create_dir_exists(self):
        absolute_path = os.path.join(os.getcwd(), "./tests/already/here")
        os.makedirs(absolute_path)
        # Calling the structure class
        s = Structure(self.project_root, "./tests/already/here", self.template, self.file_name_format)
        s.full_path = absolute_path

        try:
            s.create_dir()
        except FileExistsError:
            self.fail("create_directories failed because directories already exist")
        finally:
            shutil.rmtree("./tests/already/")
