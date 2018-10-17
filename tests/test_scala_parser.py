import os
import unittest

from wrapper_writer.code_elements import Method
from wrapper_writer.parsers import ScalaParser


class TestScalaParser(unittest.TestCase):
    sum_columns_docstring = """This function takes in a DataFrame and then adds a new column to it which holds the values of columnA + columnB. This is calculated by calling the sumColumns function when adding the new column."""

    two_docstring = """This function takes in two integers and multiplies them together and return the outcome."""

    testing_docstring = """This function takes in a list of stings and a string."""

    filter_on_list_docstring = """This function calls a protected function which filters the data based on where the targetCol doesn't have values that are in the values parameter."""

    filter_func_docstring = """This function will take in a DataFrame and filter the data based on where the targetCol doesn't have values that are in the values parameter."""

    config_container = """one_method:
  sumColumns:
    params:
      df:
         default: 
         type: DataFrame
         doc: "data set need for function"
    docs: ""
    returns: DataFrame
    access: public
    other:
"""

    run_end_string = """maths:
  sum_columns:
    params:
      df:
         type: DataFrame
         default: 
         doc: "Stores all the data."
      column_a:
         type: String
         default: 
         doc: "Name of column to add."
      column_b:
         type: String
         default: 
         doc: "Name of column to add."
      new_col:
         type: String
         default: 
         doc: "Name of new column being added to to data set, holds the values of columnA + columnB."
    docs: "This function takes in a DataFrame and then adds a new column to it which holds the values of columnA + columnB. This is calculated by calling the sumColumns function when adding the new column."
    returns: DataFrame
    access: public
    other:
  sum:
    params:
      column_a:
         type: String
         default: 
         doc: "Name of column to add."
      column_b:
         type: String
         default: 
         doc: "Name of column to add."
    docs: "This function takes in two strings, converts them to Spark columns then adds them together."
    returns: Column
    access: protected
    other:
  multiply:
    params:
      column_a:
         type: Int
         default: 
         doc: "Integer to multiply."
      column_b:
         type: Int
         default: 
         doc: "Integer to multiply."
    docs: "This function takes in two integers and multiplies them together and return the outcome."
    returns: Int
    access: protected
    other:
operations:
  filter_on_list:
    params:
      df:
         type: DataFrame
         default: 
         doc: "Stores all the data."
      target_col:
         type: String
         default: 
         doc: "Column to be filtered on."
      values:
         type: List[Int]
         default: 
         doc: "List of values to compared."
    docs: "This function calls a protected function which filters the data based on where the targetCol doesn't have values that are in the values parameter."
    returns: DataFrame
    access: public
    other:
  filter_funct:
    params:
      df:
         type: DataFrame
         default: 
         doc: "Stores all the data."
      target_col:
         type: String
         default: 
         doc: "Column to be filtered on."
      values:
         type: List[Int]
         default: 
         doc: "List of values to compared."
    docs: "This function will take in a DataFrame and filter the data based on where the targetCol doesn't have values that are in the values parameter."
    returns: DataFrame
    access: protected
    other:
"""
    test_resource_dir = os.path.join(os.getcwd(), "tests/resources/input/")
    example_dir = os.path.join(os.getcwd(), "example/src/main/scala/com/example/")

    def setUp(self):
        self.sp = ScalaParser()
        self.sp.containers = []
        self.sp.files = []

    def test_regex_parser_no_data(self):
        method = self.sp.regex_parser("")
        self.assertEqual([], method)

    def test_regex_parser_one_method(self):
        path = os.path.normpath(os.path.join(self.test_resource_dir, "one_method.scala"))
        with open(path) as f:
            data = f.read()

        method = self.sp.regex_parser(data)
        self.assertEqual("sum_columns", method[0].name)
        self.assertEqual({"column_a":  {'default': '', 'doc': 'Name of column to add.', 'type': 'String'},
                          "column_b": {'default': '', 'doc': 'Name of column to add.', 'type': 'String'},
                          "df": {'default': '', 'doc': 'Stores all the data.', 'type': 'DataFrame'},
                          "new_col": {'default': '',
                                     'doc': 'Name of new column being added to to data set, holds the values of columnA + columnB.',
                                     'type': 'String'}},
                         method[0].params)
        self.assertEqual(self.sum_columns_docstring, method[0].docs)
        self.assertEqual("DataFrame", method[0].returns)
        self.assertEqual("public", method[0].access)
        self.assertEqual({}, method[0].other)

    def test_regex_parser_no_docstring(self):
        data = "def aggColumn(df: DataFrame, col1: String, col2: String, new_col: String): DataFrame"
        method = self.sp.regex_parser(data)
        self.assertEqual("agg_column", method[0].name)
        self.assertEqual({'col1': {'default': '', 'doc': '', 'type': 'String'},
                          'col2': {'default': '', 'doc': '', 'type': 'String'},
                          'df': {'default': '', 'doc': '', 'type': 'DataFrame'},
                          'new_col': {'default': '', 'doc': '', 'type': 'String'}},
                         method[0].params)
        self.assertEqual("", method[0].docs)
        self.assertEqual("DataFrame", method[0].returns)
        self.assertEqual("public", method[0].access)
        self.assertEqual({}, method[0].other)

    def test_regex_parser_no_params(self):
        data = """/**
        * hi
        * @return DataFrame
        **/
        def aggColumn(): DataFrame = {}"""
        method = self.sp.regex_parser(data)
        self.assertEqual("agg_column", method[0].name)
        self.assertEqual({}, method[0].params)
        self.assertEqual("hi", method[0].docs)
        self.assertEqual("DataFrame", method[0].returns)
        self.assertEqual("public", method[0].access)
        self.assertEqual({}, method[0].other)

    def test_regex_parser_no_methods(self):
        method = self.sp.regex_parser("object Fred {}")
        self.assertEqual([], method)

    def test_regex_parser_no_return_type(self):
        data = """/**
        * hi
        * @param df DataFrame - data set need for function
        **/
        def aggColumn(df: DataFrame): = {}"""
        method = self.sp.regex_parser(data)

        self.assertEqual("agg_column", method[0].name)
        self.assertEqual({"df": {"default":"", "type":"DataFrame", "doc": "data set need for function"}}, method[0].params)
        self.assertEqual("hi", method[0].docs)
        self.assertEqual("", method[0].returns)
        self.assertEqual("public", method[0].access)
        self.assertEqual({}, method[0].other)

    def test_regex_parser_multiplies(self):
        path = os.path.normpath(os.path.join(self.test_resource_dir, "mixture.scala"))
        with open(path) as f:
            data = f.read()

        method = self.sp.regex_parser(data)

        self.assertEqual("sum_columns", method[0].name)
        self.assertEqual("sum", method[1].name)
        self.assertEqual("two", method[2].name)
        self.assertEqual("testing", method[3].name)
        self.assertEqual("filter_on_list", method[4].name)
        self.assertEqual("filter_funct", method[5].name)

        self.assertEqual({"df": {'default': '', 'doc': 'Stores all the data.', 'type': 'DataFrame'},
                          "column_a": {'default': '', 'doc': 'Name of column to add.', 'type': 'String'},
                          "column_b": {'default': '', 'doc': 'Name of column to add.', 'type': 'String'},
                          "new_col": {'default': '', 'doc': 'Name of new column being added to to data set, holds the values of columnA + columnB.',
                                      'type': 'String'}},
                         method[0].params)
        self.assertEqual({"column_a": {'default': '', 'doc': 'Stores all the data.', 'type': 'String'},
                          "column_b": {'default': '', 'doc': 'Name of column to add.', 'type': 'String'}},
                         method[1].params)
        self.assertEqual({}, method[2].params)
        self.assertEqual({"colb": {'default': '', 'doc': '', 'type': 'List[String]'},
                          "cola": {'default': '"hello"', 'doc': '', 'type': 'String'}}, method[3].params)
        self.assertEqual({"df": {'default': '', 'doc': 'Stores all the data.', 'type': 'DataFrame'},
                          "target_col": {'default': '', 'doc': 'Column to be filtered on.',  'type': 'String'},
                          "values": {'default': '',  'doc': 'List of values to compared.', 'type': 'List[Int]'}},
                         method[4].params)
        self.assertEqual({"df":{'default': '', 'doc': 'Stores all the data.', 'type': 'DataFrame'},
                          "target_col": {'default': '', 'doc': 'Column to be filtered on.',  'type': 'String'},
                          "values": {'default': '',  'doc': 'List of values to compared.', 'type': 'List[Int]'}},
                         method[5].params)

        self.assertEqual("DataFrame", method[0].returns)
        self.assertEqual("Column", method[1].returns)
        self.assertEqual("list[Int]", method[2].returns)
        self.assertEqual("", method[3].returns)
        self.assertEqual("DataFrame", method[4].returns)
        self.assertEqual("DataFrame", method[5].returns)

        self.assertEqual(self.sum_columns_docstring, method[0].docs)
        self.assertEqual("", method[1].docs)
        self.assertEqual(self.two_docstring, method[2].docs)
        self.assertEqual(self.testing_docstring, method[3].docs)
        self.assertEqual(self.filter_on_list_docstring, method[4].docs)
        self.assertEqual(self.filter_on_list_docstring, method[4].docs)
        self.assertEqual(self.filter_func_docstring, method[5].docs)

        for i in range(5):
            self.assertEqual("public", method[i].access)
        self.assertEqual("protected", method[5].access)

        for i in range(6):
            self.assertEqual({}, method[i].other)

    def test_create_containers_no_methods(self):
        path = os.path.normpath(os.path.join(self.test_resource_dir, "one_method.scala"))
        self.sp.create_containers([], path)
        self.assertEqual([], self.sp.containers)
        self.assertEqual("", self.sp.config)

    def test_create_containers_no_file_path(self):
        with self.assertRaises(Exception) as none_message:
            self.sp.create_containers([], None)

        err_none = str(none_message.exception)
        self.assertEqual("File path is : None", err_none)

        with self.assertRaises(Exception) as empty_message:
            self.sp.create_containers([], "")
        err_empty = str(empty_message.exception)
        self.assertEqual("File path is : ", err_empty)

    def test_create_containers(self):
        path = os.path.normpath(os.path.join(self.test_resource_dir, "one_method.scala"))
        methods = [Method("sumColumns", {"df": {"default":"", "type":"DataFrame", "doc": "data set need for function"}}, "", "DataFrame")]
        self.sp.create_containers(methods, path)

        self.assertEqual(self.config_container, self.sp.containers[0])

    def test_run_empty(self):
        with self.assertRaises(Exception) as error:
            self.sp.run()
        message = str(error.exception)
        self.assertEqual("Config string is empty", message)

    def test_run_true(self):
        try:
            path1 = os.path.normpath(os.path.join(self.example_dir, "Maths.scala"))
            path2 = os.path.normpath(os.path.join(self.example_dir, "Operations.scala"))
            self.sp.files = [path1, path2]
            self.sp.run()
            self.assertTrue(os.path.isfile("method_config.yml"))

            with open("method_config.yml") as f:
                data = f.read()

            self.assertEqual(self.run_end_string, data)
        finally:
            os.remove("./method_config.yml")

    def test_parameter_dictionary_wrong_types(self):
        params = self.sp.parameter_dictionary(None, None)
        self.assertEqual(params, {})

        params = self.sp.parameter_dictionary([''], [''])
        self.assertEqual(params, {})

        params = self.sp.parameter_dictionary([], [])
        self.assertEqual(params, {})

    def test_parameter_dictionary_no_doc(self):
        parameter_match = ["df:DataFrame"]
        params = self.sp.parameter_dictionary(parameter_match, [])
        self.assertEqual({"df": {"type":"DataFrame", "default":"", "doc":""}}, params)

        params = self.sp.parameter_dictionary(parameter_match, None)
        self.assertEqual({"df": {"type": "DataFrame", "default": "", "doc": ""}}, params)

        params = self.sp.parameter_dictionary(parameter_match, [''])
        self.assertEqual({"df": {"type": "DataFrame", "default": "", "doc": ""}}, params)

    def test_parameter_dictionary_default_string(self):
        parameter_match = ["df:DataFrame", 'column:String = "Fred"']
        params = self.sp.parameter_dictionary(parameter_match, [])
        self.assertEqual({"df": {"type": "DataFrame", "default": "", "doc": ""},
                          "column": {"type":"String", "default":'"Fred"', "doc":""}}, params)

    def test_parameter_dictionary_default_int(self):
        parameter_match = ["df:DataFrame", 'value:Int = 2']
        params = self.sp.parameter_dictionary(parameter_match, [])
        self.assertEqual({"df": {"type": "DataFrame", "default": "", "doc": ""},
                          "value": {"type":"Int", "default":'2', "doc":""}}, params)


    def test_parameter_dictionary_default_list_int(self):
        parameter_match = ["df:DataFrame", 'values:List[Int] = [2, 3, 4]']
        params = self.sp.parameter_dictionary(parameter_match, [])
        self.assertEqual({"df": {"type": "DataFrame", "default": "", "doc": ""},
                          "values": {"type":"List[Int]", "default":'[2, 3, 4]', "doc":""}}, params)

    def test_parameter_dictionary_default_seq_string(self):
        parameter_match = ["df:DataFrame", 'columns:Seq[String] = Seq("Fred", "molly")']
        params = self.sp.parameter_dictionary(parameter_match, [])
        self.assertEqual({"df": {"type": "DataFrame", "default": "", "doc": ""},
                          "columns": {"type":"Seq[String]", "default":'Seq("Fred", "molly")', "doc":""}}, params)


    def test_parameter_dictionary_doc(self):
        parameter_match = ["df:DataFrame", 'column:String = "Fred"']
        parameter_doc = ['@param df DataFrame - Data going in.', '@param column String - column name.']
        params = self.sp.parameter_dictionary(parameter_match, parameter_doc)
        self.assertEqual({"df": {"type": "DataFrame", "default": "", "doc": "Data going in."},
                          "column": {"type":"String", "default":'"Fred"', "doc":"column name."}}, params)

    def test_parameter_dictionary_doc_without_dash(self):
        parameter_match = ["df:DataFrame", 'column:String = "Fred"']
        parameter_doc = ['@param df DataFrame Data going in.', '@param column String column name.']
        params = self.sp.parameter_dictionary(parameter_match, parameter_doc)
        self.assertEqual({"df": {"type": "DataFrame", "default": "", "doc": "Data going in."},
                          "column": {"type":"String", "default":'"Fred"', "doc":"column name."}}, params)


    def test_parameter_dictionary_withput_descriptions(self):
        parameter_match = ["df:DataFrame", 'column:String = "Fred"']
        parameter_doc = ['@param df DataFrame', '@param column String']
        params = self.sp.parameter_dictionary(parameter_match, parameter_doc)
        self.assertEqual({"df": {"type": "DataFrame", "default": "", "doc": ""},
                          "column": {"type":"String", "default":'"Fred"', "doc":""}}, params)

