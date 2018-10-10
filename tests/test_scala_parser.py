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

    method_signature_no_space = "def aggColumn(df:DataFrame,col1:String,col2:String,newCol:String): DataFrame"

    method_config = {'FilterOnList': {
        'filterFunct': {'params': {'df': 'DataFrame', 'targetCol': 'String', 'values': 'List[Int]'},
                        'returns': 'DataFrame'}}}

    project_root = os.getcwd()

    goal_dir_raw = os.path.join(project_root, "example/src/main/scala/com/example/Maths.scala")

    goal_dir = os.path.normpath(goal_dir_raw)

    def test_find_method_regex(self):
        """
        Assert the regex search return is not None
        """
        sp = ScalaParse()
        result = sp.find_method_regex(self.expected_code)
        res_tup = tuple(result)
        self.assertIsNotNone(res_tup)

    def test_multi_process(self):
        """
        Assert the file output, matches the expected,
        The test will check if multiprocess function appends the expected string block to the container
        Delete file if there are the same, raise an assertion error if not
        :return:
        """
        sp = ScalaParse()
        sp.files = []
        sp.files.append(self.goal_dir)
        sp.multi_process()
        expected = ['Maths:\n'
                    '  sumColumns:\n'
                    '    params:\n'
                    '      df: DataFrame\n'
                    '      columnA: String\n'
                    '      columnB: String\n'
                    '      newCol: String\n'
                    '    docs:  This function calls a protected function which filters the data '
                    "based on where the targetCol doesn't have values that are in the values "
                    'parameter.\n'
                    '@param df DataFrame - Stores all the data.\n'
                    '@param targetCol String - Column to be filtered on.\n'
                    '@param values List[Int] - List of values to compared.\n'
                    '@return DataFrame\n'
                    '    returns: DataFrame\n'
                    '    other:\n'
                    '  sum:\n'
                    '    params:\n'
                    '      columnA: String\n'
                    '      columnB: String\n'
                    '    docs:  This function will take in a DataFrame and filter the data based '
                    "on where the targetCol doesn't have values that are in the values "
                    'parameter.\n'
                    '@param df DataFrame - Stores all the data.\n'
                    '@param targetCol String - Column to be filtered on.\n'
                    '@param values List[Int] - List of values to compared.\n'
                    '@return DataFrame\n'
                    '    returns: Column\n'
                    '    other:\n'
                    '  multiply:\n'
                    '    params:\n'
                    '      columnA: Int\n'
                    '      columnB: Int\n'
                    '    docs:  This function will take in a DataFrame and filter the data based '
                    "on where the targetCol doesn't have values that are in the values "
                    'parameter.\n'
                    '@param df DataFrame - Stores all the data.\n'
                    '@param targetCol String - Column to be filtered on.\n'
                    '@param values List[Int] - List of values to compared.\n'
                    '@return DataFrame\n'
                    '    returns: Int\n'
                    '    other:\n']
        self.assertEqual(expected, sp.containers)

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
        result = sp.extract_params(self.method_signature_no_space)
        expected = {'df': 'DataFrame', 'col1': 'String', 'col2': 'String', 'newCol': 'String'}
        self.assertEqual(expected, result)

    def test_extract_params_not_found(self):
        """
        Assert that the method params dictionary object is same as expected
        :return:
        """
        sp = ScalaParse()
        result = sp.extract_params("def aggColumn(): DataFrame")
        expected = {}
        self.assertEqual(expected, result)

    def test_docstring_found(self):
        """
        Assert that the docstring found is same as expected
        :return:
        """
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

    def test_docstring_not_found(self):
        """
        Assert the docstring is not not found
        :return:
        """
        data = "def func(df:DataFrame, col:String): DataFrame"
        no_doc = ScalaParse()
        no_doc.doc_strings = []
        no_doc.find_doc_string(data)
        self.assertFalse(no_doc.doc_strings)