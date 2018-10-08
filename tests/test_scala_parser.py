import unittest
import yaml
import os
import mock
from wrapper_writer.scala_parser import ScalaParse, App


class TestScalaParser(unittest.TestCase):
    expected_code = (""" 
        package com.example

import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions.col

object FilterOnList {

  def filterOnList(df: DataFrame, targetCol: String, values: List[Int]): DataFrame = {
    filterFunct(df, targetCol, values)
  }

  protected def filterFunct(df: DataFrame, targetCol: String, values: List[Int]): DataFrame = {
    df.where(!col(targetCol).isin(values: _*))
  }
}

        """).strip()

    config_name = "config.yml"

    method_signature = "def aggColumn(df: DataFrame, col1: String, col2: String, newCol: String): DataFrame"

    method_config = {'FilterOnList': {'filterFunct': {'params': {'df': 'DataFrame', 'targetCol': 'String', 'values': 'List[Int]'}, 'returns': 'DataFrame'}}}

    project_root = os.getcwd()

    goal_dir_raw = os.path.join(project_root, "tests/resources/input/FilterOnList.scala")

    goal_dir = os.path.normpath(goal_dir_raw)

    def test_read_scala_file(self):
        """
        Assert that the functions reads in the input file correctly
        """
        sp = ScalaParse(filename=self.goal_dir, config_name=self.config_name)
        res = sp.read_scala_file()
        self.assertEqual(self.expected_code, res)

    def test_find_method_regex(self):
        """
        Assert the regex search return is not None
        """
        sp = ScalaParse(filename=self.goal_dir, config_name=self.config_name)
        result = sp.find_method_regex()
        res_tup = tuple(result)
        print(res_tup)
        self.assertIsNotNone(res_tup)


    def test_multi_process(self):
        """
        Assert the file output, matches the expected,
        The test will write the output file, read its contents, read the contents of expected file, compare the two.
        Delete file if there are the same, raise an assertion error if not
        :return:
        """
        sp = ScalaParse(filename=self.goal_dir, config_name=self.config_name)
        sp.multi_process()
        with open("config.yml", 'r') as c:
            config = yaml.load(c)
        self.assertDictEqual(self.method_config, config)
        os.remove(self.config_name)

    def test_extract_return_type(self):
        """
        Assert that the return type string object is same as expected
        :return:
        """
        sp = ScalaParse(filename=self.goal_dir, config_name=self.config_name)
        result = sp.extract_return_type(self.method_signature)
        expected = "DataFrame"
        self.assertEqual(expected, result)

    def test_extract_method_name(self):
        """
        Assert that the method name string object is same as expected
        :return:
        """
        sp = ScalaParse(filename=self.goal_dir, config_name=self.config_name)
        result = sp.extract_method_name(self.method_signature)
        expected = "aggColumn"
        self.assertEqual(expected, result)

    def test_extract_params(self):
        """
        Assert that the method params dictionary object is same as expected
        :return:
        """
        sp = ScalaParse(filename=self.goal_dir, config_name=self.config_name)
        result = sp.extract_params(self.method_signature)
        expected = {'df': 'DataFrame', 'col1': 'String', 'col2': 'String', 'newCol': 'String'}
        self.assertEqual(expected, result)


class TestApp(unittest.TestCase):

    @mock.patch('wrapper_writer.scala_parser.os.path')
    @mock.patch('wrapper_writer.scala_parser.os')
    def test_delete_config(self, mock_os, mock_path):

        # set up the mock
        mock_path.isfile.return_value = False
        app = App(config_name="config.yml")
        app.delete_config()

        # test that the remove call was not called
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present")


if __name__ == "__main__":
    unittest.main(verbosity=2)