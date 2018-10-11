import os
import re

from wrapper_writer.container import Container
from wrapper_writer.method import Method


class Parser:
    """
    The Parser class contains the details and functionality associated with parsing one or more files into a config file

    :param config_name: The name of the config file to write.
    :type config_name: str
    :param append_config: Whether to append to the config file or to overwrite it
    :type append_config: bool
    """

    containers = []  #: The list which holds all the container classes.
    files = []  #: The list which holds all the absolute paths to the files.

    def __init__(self, config_name="method_config.yml", append_config="w"):
        self.config_name = config_name
        self.append_config = append_config

    def get_files(self, directory, target_format):
        """
        This method gets all files in a given directory that matches a given format and appends them to the files list.

        :param directory: The absolute path of the directory to look for files within
        :type directory: str
        :param target_format: A regex string that defines the naming convention of the files to parse.
        :type target_format: str
        """

        all_files = os.listdir(directory)

        regex = re.compile(target_format)

        selected_files = list(filter(regex.search, all_files))

        absolute_paths = [os.path.join(directory, f) for f in selected_files]

        self.files.extend(absolute_paths)

    @staticmethod
    def read_file(file_path):
        """
        This method reads a file_path and returns its contents as a string

        :param file_path: The absolute path to the file to open
        :type file_path: str
        :return: str
        """
        with open(file_path) as f:
            return f.read()

    def write_config(self):
        """
        This method writes the current list of containers to the config file.
        """
        combined = ""

        for i in self.containers:
            combined += i
        with open(self.config_name, self.append_config) as txt_file:
            txt_file.write(combined)

    def delete_config(self):
        """
        This function will check if a file exist then delete it
        :return:
        """
        print("Checking if file exists ...")
        if os.path.isfile(self.config_name):
            os.remove(self.config_name)
        else:
            print("The config file does not exists")


class ScalaParse(Parser):
    """
    This ScalaParse class parses a scala file, extracts the method elements and writes them out to a config file
    :param filename: The name of the file to parse
    :param config_name: The name of the yaml config file
    :param append_config: boolean value, True will overwrite an existing file, False will append to file
    """

    doc_strings = []  #: This is a list of all the doc_strings gathered from the regex

    def find_method_regex(self, retrieve_data):
        """
        This function will find the raw method signature from file to be parsed
        :return: iterable object with all methods found
        """
        pattern = re.compile("def (\w+)\((.*)\): (\w+)", re.MULTILINE)
        try:
            pattern2 = pattern.finditer(retrieve_data)
        except:
            print("Nothing In There")
        return pattern2

    def find_doc_string(self, data):
        """
        This function will check the data for the relevant regex string, in order to pick out the doc strings from a
        function.

        :param data: The data given as a string for the regex to read.
        """
        matches = re.finditer(r"/\*\*([\s,\w,\*,@,\+\.,='\[\]\-/%]*)\*/", data, re.MULTILINE)
        for match in matches:
            group = match.group(1)
            if group:
                doc = group.replace("*", "").replace("\n     @", "\n@").replace("\n    ", "").replace("\n     ", " ")
            else:
                doc = None

            # Temporary fix to remove things starting with a @
            doc = re.sub("\n?@.*\n?", "", doc)

            self.doc_strings.append(doc.strip())

    @staticmethod
    def extract_return_type(raw_res):
        """
        This function extracts the return type of a method
        :param raw_res: A method signature from the file to be parsed
        :return: return_type: String object of the return type
        """
        first, *middle, last = raw_res.split()
        return_type = last
        return return_type

    @staticmethod
    def extract_method_name(raw_res):
        """
        The function will use regex to extract the method name from the logic code
        :param raw_res: A method signature from the file to be parsed
        :return: clean_func_name: String object of the function name
        """
        func_name = r"def (\w+)"
        func_name_find = re.search(func_name, raw_res)
        fun_name_raw = func_name_find.group()
        clean_func_name = fun_name_raw.replace("def ", "")
        return clean_func_name

    @staticmethod
    def extract_params(raw_res):
        """
        This function will use regex to extract the parameters from the logic code
        :param raw_res: method signature from the file to be parsed
        :return new_dict: A dictionary containing the parameters
        """
        retrieve_params = r"\((.*)\)"
        retrieve_params_find = re.search(retrieve_params, raw_res)
        retrieve_params = retrieve_params_find.group(1)
        em_l = []
        remove_space = {}
        if not retrieve_params:
            return {}
        else:
            for x in retrieve_params.split(','):
                em_l.append(x)
            s = dict(s.split(":") for s in em_l)
            for k, v in s.items():
                s[k] = v.lstrip()
                remove_space = {k.lstrip(): v for k, v in s.items()}
            return remove_space

    def multi_process(self):
        """
        This function will process each method found and write it to a yaml file
        :return:
        """
        for filepath in self.files:
            retrieve_data = self.read_file(filepath)
            self.find_doc_string(retrieve_data)
            all_found = self.find_method_regex(retrieve_data)
            matches = tuple(all_found)
            count = 0
            if not matches:
                raise Exception("No Methods Found")
            container_methods = []
            for i in matches:
                ig = i.group()
                base_raw = os.path.basename(filepath)
                container_name = os.path.splitext(base_raw)[0]
                return_type = self.extract_return_type(ig)
                method_name = self.extract_method_name(ig)
                params = self.extract_params(ig)
                if self.doc_strings == None:
                    docs = ""
                else:
                    docs = self.doc_strings[count]
                one_method = Method(method_name, params, docs, return_type)
                container_methods.append(one_method)
                count = +1
            one_container = Container(container_name, container_methods)
            cc = one_container.create_config()
            self.containers.append(cc)