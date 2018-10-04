import re
import yaml
import os
import glob
import sys


class ScalaParse:
    """
    This ScalaParse class parses a scala file, extracts the method elements and writes them out to a config file
    :param filename: The name of the file to parse
    :param config_name: The name of the yaml config file
    :param append_config: boolean value, True will overwrite an existing file, False will append to file
    """

    def __init__(self, filename, config_name, append_config=False):
        self.filename = filename
        self.config_filename = config_name
        self.if_config_exists = append_config

    def read_file(self):
        """

        :return:
        """
        try:
            with open(self.filename) as logic_file:
                data = logic_file.read()
            return data
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            sys.exit(1)

    def prepare_files(self):
        """
        This funciton will all user to delete the contents of the file it exists
        :return:
        """
        print("Checking if file exists ...")
        if os.path.exists(self.config_filename):
            os.remove(self.config_filename)
        else:
            print("The config file does not exists")

    def find_method_regex(self):
        """
        This function will find method raw method signature from file to be parsed
        :return: iterable object with all methods found
        """
        retrieve_data = self.read_file()
        if not self.if_config_exists:
            self.prepare_files()
        ptrn = re.compile("def (\w+)\((.*)\): (\w+)", re.MULTILINE)
        try:
            ptrn2 = ptrn.finditer(retrieve_data)
        except:
            print("Nothing In There")
        # print(ptrn2)
        return ptrn2

    def multi_process(self):
        """
        This function will process each method found and write it to a yaml file
        :return:
        """
        all_found = self.find_method_regex()
        matches = tuple(all_found)
        print(matches)
        if not matches:
            raise Exception("No Methods Found")
        for i in matches:
            ig = i.group()
            return_type = self.extract_return_type(ig)
            method_name = self.extract_method_name(ig)
            params = self.extract_params(ig)
            data ={"container": {method_name: {"params": params, "return_type": return_type}}}
            print(self.if_config_exists)
            with open(self.config_filename, 'a') as yaml_file:
                yaml.dump(data, yaml_file, default_flow_style=False)

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


class App:
    """
    This App class orchestrates the scala parser application
    :param folder: String object of the folder path which is provided by the user to indicate where files live
    :param file: String object if the file to be parsed
    :param file_extension: String object of file extension to look for
    """

    def __init__(self, folder=None, logic_file=None, file_extension="*.scala", config_name="config_sadhg.yml", append_config=False):
        self.folder = folder
        self.file = logic_file
        self.file_extension = file_extension
        self.config_file = config_name
        self.append_config = append_config

    def prepare_input(self):
        """
        This function will prepare the use input,
        :return: all files to be parsed
        """
        all_files = []
        prep_ends_with = self.file_extension[1:]
        if not (self.folder or self.file):
            raise TypeError("Provide File or Directory")
        if self.folder and not self.file:
            if os.path.exists(self.folder):
                self.folder += self.file_extension

                for files in glob.glob(self.folder):
                    if files.endswith(prep_ends_with):
                        all_files.append(files)
                return all_files
            else:
                print("Throw exception here directory doesnt exist")
        elif self.file and not self.folder:

            all_files.append(self.file)
            return all_files

    def run_scala(self):
        scala_files_to_run = self.prepare_input()
        for p in scala_files_to_run:
            x = ScalaParse(p, self.config_file, self.append_config)
            x.multi_process()

    def run_python(self):
        pass

    def run_r(self):
        pass


