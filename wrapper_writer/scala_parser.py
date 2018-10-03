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
        try:
            with open(self.filename) as logic_file:
                data = logic_file.read()
            return data
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            sys.exit(1)

    def prepare_files(self):
        print("Checking if file exists ...")
        if os.path.exists(self.config_filename):
            os.remove(self.config_filename)
        else:
            print("The config file does not exists")

    def find_method_regex(self):
        retrieve_data = self.read_file()
        # if not self.if_config_exists:
        #     self.prepare_files()
        ptrn = re.compile("def (\w+)\((.*)\): (\w+)", re.MULTILINE)
        try:
            ptrn2 = ptrn.finditer(retrieve_data)
        except:
            print("Nothing In There")
        print(ptrn2)
        return ptrn2

    def multi_process(self):
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
            data ={"methods": {method_name: {"params": params, "return_type": return_type}}}
            print(self.if_config_exists)
            with open(self.config_filename, 'a') as yaml_file:
                yaml.dump(data, yaml_file, default_flow_style=False)

    @staticmethod
    def extract_return_type(raw_res):
        first, *middle, last = raw_res.split()
        return_type = last
        return return_type

    @staticmethod
    def extract_method_name(raw_res):
        func_name = r"def (\w+)"
        func_name_find = re.search(func_name, raw_res)
        fun_name_raw = func_name_find.group()
        clean_func_name = fun_name_raw.replace("def ", "")
        return clean_func_name

    @staticmethod
    def extract_params(raw_res):
        retrieve_params = r"\((.*)\)"
        retrieve_params_find = re.search(retrieve_params, raw_res)
        retrieve_params_raw = retrieve_params_find.group()
        retrieve_params_clean = retrieve_params_raw[1:-1]
        dict_by_comma = dict(item.split(":") for item in retrieve_params_clean.split(","))
        for k, v in dict_by_comma.items():
            dict_by_comma[k] = v.lstrip()
            new_dict = {k.lstrip(): v for k, v in dict_by_comma.items()}
        return new_dict


class Orchestrator:
    """
    This class orchestrates the scala parser application
    """

    def __init__(self, folder=None, logic_file=None, file_extension="\\*"):
        self.folder = folder
        self.file = logic_file
        self.file_extension = file_extension

    def crossroad(self):
        if not (self.folder or self.file):
            raise TypeError("Provide File or Directory")
        if self.folder and not self.file:
            if os.path.exists(self.folder):
                self.folder += self.file_extension
                scala_files = []
                for files in glob.glob(self.folder):
                    if files.endswith(".scala"):
                        scala_files.append(files)
                for p in scala_files:
                    x = ScalaParse(p, "config_redir.yml")
                    x.multi_process()
            else:
                print("Throw exception here directory doesnt exist")
        elif self.file and not self.folder:
            y = ScalaParse(self.file, "config_solo.yml")
            y.multi_process()


if __name__ == '__main__':
    t = Orchestrator(folder="C:\\Users\\Ian Edwards\\projects\\dap-s\\wrapper-writer\\wrapper-writer\\example\\src\\main\\scala\\com\\example")
    t.crossroad()

