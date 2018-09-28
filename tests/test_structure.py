from unittest import TestCase

import os

from wrapper_writer.structure import Structure

class TestStructure(TestCase):
    path = "./tests/dir/tests"
    template = ""
    file_name_format = ""

    @classmethod
    def tearDownClass(cls):
        absolute_path = os.getcwd()
        directories = cls.path.split("\\")
        for i in range(len(directories), 1, -1):
            latest_path = "\\".join(directories[0:i])
            os.rmdir(os.path.join(absolute_path,latest_path))

    def test_create_path(self):
        absolute_path = os.path.join(os.getcwd(), self.path)

        # Calling the structure class
        s = Structure(self.path, self.template, self.file_name_format)
        s.create_path()
        full_path = s.full_path

        self.assertEquals(absolute_path, full_path)

    def test_create_dir(self):
        absolute_path = os.path.join(os.getcwd(), self.path)

        # Calling the structure class
        s = Structure(self.path, self.template, self.file_name_format)
        s.create_path()
        s.create_dir()

        self.assertTrue(os.path.isdir(absolute_path))

    def test_create_dir_exists(self):
        absolute_path = os.path.join(os.getcwd(), "./tests/already/here")
        os.makedirs(absolute_path)
        # Calling the structure class
        s = Structure("./tests/already/here", self.template, self.file_name_format)
        s.create_path()

        try:
            s.create_dir()
        except FileExistsError:
            self.fail("create_directories failed because directories already exist")



