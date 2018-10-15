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
      df: DataFrame
    docs: ""
    returns: DataFrame
    other:
"""

    run_end_string = """Maths:
  sumColumns:
    params:
      df: DataFrame
      columnA: String
      columnB: String
      newCol: String
    docs: "This function takes in a DataFrame and then adds a new column to it which holds the values of columnA + columnB. This is calculated by calling the sumColumns function when adding the new column."
    returns: DataFrame
    other:
  sum:
    params:
      columnA: String
      columnB: String
    docs: "This function takes in two strings, converts them to Spark columns then adds them together."
    returns: Column
    other:
  multiply:
    params:
      columnA: Int
      columnB: Int
    docs: "This function takes in two integers and multiplies them together and return the outcome."
    returns: Int
    other:
Operations:
  filterOnList:
    params:
      df: DataFrame
      targetCol: String
      values: List[Int]
    docs: "This function calls a protected function which filters the data based on where the targetCol doesn't have values that are in the values parameter."
    returns: DataFrame
    other:
  filterFunct:
    params:
      df: DataFrame
      targetCol: String
      values: List[Int]
    docs: "This function will take in a DataFrame and filter the data based on where the targetCol doesn't have values that are in the values parameter."
    returns: DataFrame
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

        self.assertEqual("sumColumns", method[0].name)
        self.assertEqual({"columnA":  {'default': '', 'doc': 'Name of column to add. ', 'type': 'String'},
                          "columnB": {'default': '', 'doc': 'Name of column to add. ', 'type': 'String'},
                          "df": {'default': '', 'doc': 'Stores all the data. ', 'type': 'DataFrame'},
                          "newCol": {'default': '',
                                     'doc': 'Name of new column being added to to data set, holds the values of columnA + columnB.',
                                     'type': 'String'}},
                         method[0].params)
        self.assertEqual(self.sum_columns_docstring, method[0].docs)
        self.assertEqual("DataFrame", method[0].returns)

    def test_regex_parser_no_docstring(self):
        data = "def aggColumn(df: DataFrame, col1: String, col2: String, newCol: String): DataFrame"
        method = self.sp.regex_parser(data)
        self.assertEqual("aggColumn", method[0].name)
        self.assertEqual({"df": "DataFrame", "col1": "String", "col2": "String", "newCol": "String"},
                         method[0].params)
        self.assertEqual("", method[0].docs)
        self.assertEqual("DataFrame", method[0].returns)

    def test_regex_parser_no_params(self):
        data = """/**
        * hi
        * @return DataFrame
        **/
        def aggColumn(): DataFrame = {}"""
        method = self.sp.regex_parser(data)
        self.assertEqual("aggColumn", method[0].name)
        self.assertEqual({}, method[0].params)
        self.assertEqual("hi", method[0].docs)
        self.assertEqual("DataFrame", method[0].returns)

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
        print(method)
        self.assertEqual("aggColumn", method[0].name)
        self.assertEqual({"df": {"default":"", "type":"DataFrame", "doc": "data set need for function"}}, method[0].params)
        self.assertEqual("hi", method[0].docs)
        self.assertEqual("", method[0].returns)

    def test_regex_parser_multiplies(self):
        path = os.path.normpath(os.path.join(self.test_resource_dir, "mixture.scala"))
        with open(path) as f:
            data = f.read()

        method = self.sp.regex_parser(data)

        self.assertEqual("sumColumns", method[0].name)
        self.assertEqual("sum", method[1].name)
        self.assertEqual("two", method[2].name)
        self.assertEqual("testing", method[3].name)
        self.assertEqual("filterOnList", method[4].name)
        self.assertEqual("filterFunct", method[5].name)



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
        methods = [Method("sumColumns", {"df": "DataFrame"}, "", "DataFrame")]
        self.sp.create_containers(methods, path)

        self.assertEqual(self.config_container, self.sp.containers[0])

    def test_run_empty(self):
        with self.assertRaises(Exception) as error:
            self.sp.run()
        message = str(error.exception)
        self.assertEqual("Config string is empty", message)

    def test_run_true(self):
        #try:
        path1 = os.path.normpath(os.path.join(self.example_dir, "Maths.scala"))
        path2 = os.path.normpath(os.path.join(self.example_dir, "Operations.scala"))
        self.sp.files = [path1, path2]
        self.sp.run()
        self.assertTrue(os.path.isfile("method_config.yml"))

        with open("method_config.yml") as f:
            data = f.read()

        self.assertEqual(self.run_end_string, data)
        #finally:
    # os.remove("./method_config.yml")




    def test_parameter_dictionary_no_doc(self):
        parameter_match = ["df:DataFrame", "colA:String"]
        params = self.sp.parameter_dictionary(parameter_match, [])
        self.assertEqual({"df": {"type":"DataFrame", "default":"", "doc":""},
                          "colA":{"type":"String", "default":"", "doc":""}}, params)

    def test_parameter_dictionary_no_param(self):
        params = self.sp.parameter_dictionary([""], [])
        self.assertEqual({}, params)

    def test_parameter_dictionary_defaults(self):
        parameter_match = ["df:DataFrame", "colA:String='Ted'"]
        params = self.sp.parameter_dictionary(parameter_match, [])
        self.assertEqual({"df": {"type":"DataFrame", "default":"", "doc":""},
                          "colA":{"type":"String", "default":"'Ted'", "doc":""}}, params)