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

    def test_read_scala_file(self):
        """Asset that the functions reads in the input file correctly"""

        sp = ScalaParse(filename=self.path, config_name="config.yaml")
        res = sp.read_scala_file()
        # print(res)
        self.assertEqual(self.expected_code, res)

    def test_find_method_regex(self):
        sp = ScalaParse(filename=self.path)
        result = sp.find_method_regex()

    def test_multi_process(self):
        sp = ScalaParse(filename=self.path)
        result = sp

    def test_extract_return_type(self):
        sp = ScalaParse(filename=self.path)
        result = sp.extract_return_type()

    def test_extract_method_name(self):
        sp = ScalaParse(filename=self.path)
        result = sp.extract_method_name()

    def test_extract_params(self):
        sp = ScalaParse(filename=self.path)
        result = sp.extract_params()

class TestApp(TestCase):

    def test_prepare_input(self):
        a = App()
        result = a.prepare_input()



