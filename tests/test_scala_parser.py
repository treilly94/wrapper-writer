import os
import unittest

import yaml

from wrapper_writer.scala_parser import ScalaParse


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

    method_config = {'FilterOnList': {
        'filterFunct': {'params': {'df': 'DataFrame', 'targetCol': 'String', 'values': 'List[Int]'},
                        'returns': 'DataFrame'}}}

    project_root = os.getcwd()

    goal_dir_raw = os.path.join(project_root, "tests/resources/input/FilterOnList.scala")

    goal_dir = os.path.normpath(goal_dir_raw)

    def test_find_method_regex(self):
        """
        Assert the regex search return is not None
        """
        sp = ScalaParse()
        result = sp.find_method_regex(self.expected_code)
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
        sp = ScalaParse()
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
        sp = ScalaParse()
        result = sp.extract_return_type(self.method_signature)
        expected = "DataFrame"
        self.assertEqual(expected, result)

    def test_extract_method_name(self):
        """
        Assert that the method name string object is same as expected
        :return:
        """
        sp = ScalaParse()
        result = sp.extract_method_name(self.method_signature)
        expected = "aggColumn"
        self.assertEqual(expected, result)

    def test_extract_params_found(self):
        """
        Assert that the method params dictionary object is same as expected
        :return:
        """
        sp = ScalaParse()
        result = sp.extract_params(self.method_signature)
        expected = {'df': 'DataFrame', 'col1': 'String', 'col2': 'String', 'newCol': 'String'}
        self.assertEqual(expected, result)

    def test_extract_params_nospace(self):
        """
        Assert that the method params dictionary object is same as expected
        :return:
        """
        sp = ScalaParse()
        result = sp.extract_params("def aggColumn(df:DataFrame,col1:String,col2:String,newCol:String): DataFrame")
        expected = {'df': 'DataFrame', 'col1': 'String', 'col2': 'String', 'newCol': 'String'}
        self.assertEqual(expected, result)


    def test_extract_params_notfound(self):
        """
        Assert that the method params dictionary object is same as expected
        :return:
        """
        sp = ScalaParse()
        result = sp.extract_params("def aggColumn(): DataFrame")
        expected = {}
        self.assertEqual(expected, result)

    def test_docstring_found(self):
        with open(os.path.normpath(os.path.join(os.getcwd(), "./example/src/main/scala/com/example/Operations.scala")),
                  'r') as myfile:
            data = myfile.read()
            sp = ScalaParse()
        sp.find_doc_string(data)
        expected1 = """ This function calls a protected function which filters the data based on where the targetCol doesn't have values that are in the values parameter.
@param df DataFrame - Stores all the data.
@param targetCol String - Column to be filtered on.
@param values List[Int] - List of values to compared.
@return DataFrame"""
        expected2 = """ This function will take in a DataFrame and filter the data based on where the targetCol doesn't have values that are in the values parameter.
@param df DataFrame - Stores all the data.
@param targetCol String - Column to be filtered on.
@param values List[Int] - List of values to compared.
@return DataFrame"""
        self.assertEqual(expected1, sp.doc_strings[0])
        self.assertEqual(expected2, sp.doc_strings[1])
        sp.doc_strings = []

    def test_docstring_notfound(self):
        data = "def func(df:DataFrame, col:String): DataFrame"
        no_doc = ScalaParse()
        print(data)
        print(no_doc.doc_strings)
        no_doc.doc_strings = []
        print(no_doc.doc_strings)
        no_doc.find_doc_string(data)
        print(no_doc.doc_strings)

        self.assertEqual([], no_doc.doc_strings)
