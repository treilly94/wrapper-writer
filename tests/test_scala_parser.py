import unittest
import yaml
import os
from wrapper_writer.scala_parser import App, ScalaParse


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

    reg_tuple = "(<_sre.SRE_Match object; span=(127, 207), match='def filterOnList(df: DataFrame, targetCol: String>", "<_sre.SRE_Match object; span=(268, 347), match='def filterFunct(df: DataFrame, targetCol: String,>)"

    method_signature = "def aggColumn(df: DataFrame, col1: String, col2: String, newCol: String): DataFrame"

    method_config = {'FilterOnList': {'filterFunct': {'params': {'df': 'DataFrame', 'targetCol': 'String', 'values': 'List[Int]'}, 'returns': 'DataFrame'}}}

    project_root = os.getcwd()

    goal_dir = os.path.join(project_root, "tests/resources/scala_code/FilterOnList.scala")

    def test_read_scala_file(self):
        """
        Asset that the functions reads in the input file correctly
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
        config = yaml.load(open('config.yml'))
        self.assertDictEqual(self.method_config, config)
        os.remove(self.config_name)

        # try:
        #     self.assertDictEqual(self.method_config, config)
        #
        # except AssertionError:
        #     print("The Test failed")



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


if __name__ == "__main__":
    unittest.main(verbosity=2)