from unittest import TestCase, mock

from wrapper_writer.scala_parser import Parser


class TestParser(TestCase):
    def test_get_files(self):
        with mock.patch('os.listdir') as mocked_listdir:
            # Mock the output of listdir
            mocked_listdir.return_value = ['alpha.scala', 'beta.scala', 'project.conf']

            # Call the parser
            parser = Parser()
            parser.get_files("/test/dir/", ".*\.scala")

        expected = ['alpha.scala', 'beta.scala']

        self.assertEqual(expected, parser.files)

    @mock.patch('wrapper_writer.scala_parser.os.path')
    @mock.patch('wrapper_writer.scala_parser.os')
    def test_delete_config(self, mock_os, mock_path):
        # set up the mock
        mock_path.isfile.return_value = False
        app = Parser(config_name="config.yml")
        app.delete_config()

        # test that the remove call was not called
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present")
