from unittest import TestCase

from wrapper_writer.scala_parser import App, ScalaParse


class TestScalaParser(TestCase):
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
    path = "C:\\Users\\Ian Edwards\\projects\\dap-s\\wrapper-writer\\wrapper-writer\\example\\src\\main\\scala\\com\\example\\FilterOnList.scala"

    config_name = "config.yaml"

    def test_read_scala_file(self):
        """Asset that the functions reads in the input file correctly"""

        sp = ScalaParse(filename=self.path, config_name=self.config_name)
        res = sp.read_scala_file()
        self.assertEqual(self.expected_code, res)
    #
    # def test_find_method_regex(self):
    #     """
    #     Assert the result returned i
    #     """
    #     sp = ScalaParse(filename=self.path, config_name=self.config_name)
    #     result = sp.find_method_regex()
    #     # self.assertTrue(result)
    #     # self.assertTrue(len(result))
    #     print(result)
    #
    # def test_multi_process(self):
    #     """
    #
    #     :return:
    #     """
    #     sp = ScalaParse(filename=self.path, config_name=self.config_name)
    #     # result = sp.multi_process()
    #
    # def test_extract_return_type(self):
    #     """
    #
    #     :return:
    #     """
    #     sp = ScalaParse(filename=self.path, config_name=self.config_name)
    #     # result = sp.extract_return_type()
    #
    # def test_extract_method_name(self):
    #     """
    #
    #     :return:
    #     """
    #     sp = ScalaParse(filename=self.path, config_name=self.config_name)
    #     # result = sp.extract_method_name()
    #
    # def test_extract_params(self):
    #     """
    #
    #     :return:
    #     """
    #     sp = ScalaParse(filename=self.path, config_name=self.config_name)
    #     # result = sp.extract_params()

# class TestApp(TestCase):
#
#     def test_prepare_input(self):
#         a = App()
#         result = a.prepare_input()


