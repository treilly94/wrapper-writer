import re
import os
import glob
import sys
from container import Container
from method import Method


class App:
    """
    This App class orchestrates the scala parser application
    :param folder: String object of the folder path which is provided by the user to indicate where files live
    :param file: String object if the file to be parsed
    :param file_extension: String object of file extension to look for
    """
    containers = []
    files = []

    def __init__(self, folder=None, logic_file=None, file_extension="*.scala", config_name="config_sp.yml", append_config=False):
        self.folder = folder
        self.filename = logic_file
        self.file_extension = file_extension
        self.config_file = config_name
        self.append_config = append_config

    def delete_config(self):
        """
        This function will check if a file exist then delete it
        :return:
        """
        print("Checking if file exists ...")
        if os.path.isfile(self.config_file):
            os.remove(self.config_file)
            print("File Deleted")
        else:
            print("The config file does not exists")

    def prepare_input(self):
        """
        This function will prepare the use input,
        :return: all files to be parsed
        """
        if not self.append_config:
            self.delete_config()

        # all_files = []
        prep_ends_with = self.file_extension[1:]
        if not (self.folder or self.filename):
            raise TypeError("Provide File or Directory")
        if self.folder and not self.filename:
            if os.path.exists(self.folder):
                self.folder += self.file_extension
                for files in glob.glob(self.folder):
                    if files.endswith(prep_ends_with):
                        # all_files.append(files)
                        self.files.append(files)
                # return all_files
            else:
                print("Throw exception here directory doesnt exist")
        elif self.filename and not self.folder:
            self.files.append(self.filename)
            # return all_files
        else:
            raise Exception("Please provide either a file or folder, not both")

    def write_config(self):
        for i in self.containers:
            with open(self.config_file, 'a') as txt_file:
                txt_file.write(i)


class ScalaParse(App):
    """
    This ScalaParse class parses a scala file, extracts the method elements and writes them out to a config file
    """
    def read_scala_file(self, item):
        """
        :return:
        """
        try:
            with open(item) as logic_file:
                data = logic_file.read()
            return data
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            sys.exit(1)

    def find_method_regex(self, item):
        """
        This function will find the raw method signature from file to be parsed
        :return: iterable object with all methods found
        """
        retrieve_data = self.read_scala_file(item)
        pattern = re.compile("def (\w+)\((.*)\): (\w+)", re.MULTILINE)
        try:
            pattern2 = pattern.finditer(retrieve_data)
        except:
            print("Nothing In There")
        return pattern2

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
        retrieve_params_raw = retrieve_params_find.group()
        retrieve_params_clean = retrieve_params_raw[1:-1]
        dict_by_comma = dict(item.split(":") for item in retrieve_params_clean.split(","))
        for k, v in dict_by_comma.items():
            dict_by_comma[k] = v.lstrip()
            new_dict = {k.lstrip(): v for k, v in dict_by_comma.items()}
        return new_dict

    def multi_process(self):
        """
        This function will process each method found and write it to a yaml file
        :return:
        """
        for item in self.files:
            all_found = self.find_method_regex(item)
            matches = tuple(all_found)
            if not matches:
                raise Exception("No Methods Found")
            container_methods = []
            for i in matches:
                ig = i.group()
                base_raw = os.path.basename(item)
                container_name = os.path.splitext(base_raw)[0]
                return_type = self.extract_return_type(ig)
                method_name = self.extract_method_name(ig)
                dummy_docs = "This is a doc string"
                params = self.extract_params(ig)
                one_method = Method(method_name, params, dummy_docs, return_type)
                container_methods.append(one_method)
            one_container = Container(container_name, container_methods)
            cc = one_container.create_config()
            App.containers.append(cc)

