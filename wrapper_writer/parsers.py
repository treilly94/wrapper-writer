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
    config = ""  #: The config string which holds all the data need to write to a config file.
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


class ScalaParser(Parser):
    """
    This ScalaParse class parses a scala file, extracts the method elements and writes them out to a config file
    :param filename: The name of the file to parse
    :param config_name: The name of the yaml config file
    :param append_config: boolean value, True will overwrite an existing file, False will append to file
    """

    #: The regex string specific to scala in order to get the docs, params, returns, type and name.
    regex_string = r"/\*\*([\s,\w,\*,@,\+\.,='\[\]\-/%]*)\*/|(\w+ def|def)\s(\w+)\(([\w+:\s,\[\]=\"\(\)]*)\):\s([\w\[\]]*)"

    def regex_parser(self, data):
        """
        This function takes in data as a string, then uses the regex string variable within this class. To find the
        doc strings, name, parameters, types and return type for each function within the data.
        It then stores this information as a Method class and saves all the methods as a list.
        :param data:
        :return: methods
        """
        matches = re.finditer(self.regex_string, data, re.MULTILINE)
        methods = []
        doc_string = ""
        for match in matches:
            if match.group(2) is None:
                doc_string = match.group(1).replace("*", "").replace("\n     @", "\n@").replace("\n    ", "").replace(
                    "\n     ", " ").strip()
            elif match.group(2) is not None:
                type = match.group(2)
                name = match.group(3)
                print(name)
                print(doc_string)
                params1 = match.group(4).split(",")
                print(params1)
                if params1 != ['']:
                    params = dict(item.split(":") for item in params1)
                    params = {k.lstrip(): v.lstrip() for k, v in params.items()}
                    print(params)
                else:
                    params = {}
                return_type = match.group(5)
                methods.append(Method(name, params, str(doc_string), return_type, {}))
                doc_string = ""
            else:
                print("no match found")
        return methods

    def create_containers(self, methods, file_path):
        """
        This function
        :param methods: This is a list of all the methods class within the file.
        :type methods: List[str]
        :param file_path: This is the file path to the file currently being parsed.
        :type file_path: str
        """
        invalid_files = [None, ""]
        if file_path not in invalid_files:
            container_name = file_path.split(str(os.sep))[-1].split(".")[0]
            if methods != []:
                container = Container(container_name, methods, file_path)
                self.containers.append(container.create_config())
            else:
                print("Methods for the container = ", container_name, " are not found.")
        else:
            raise Exception("File path is : " + str(file_path))

    def run(self):
        """
        This function runs the whole process provided there are files within the file list.
        """
        print("starting run")
        print(self.files)
        for file_path in self.files:
            print(file_path)
            data = self.read_file(file_path)
            methods = self.regex_parser(data)
            self.create_containers(methods, file_path)

        print("finsihed for loop")
        print(self.containers)
        if self.containers != []:
            self.write_config()
        else:
            message = "Config string is empty"
            print("Container list: ", self.containers)
            raise Exception(message)
