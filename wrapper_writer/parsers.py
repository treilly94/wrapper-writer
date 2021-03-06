import os
import re

from wrapper_writer.code_elements import Container, Method


class Parser:
    """
    The Parser class contains the details and functionality associated with parsing one or more files into a config file

    :param config_name: The name of the config file to write.
    :type config_name: str
    :param append_config: Whether to append to the config file or to overwrite it
    :type append_config: str
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
    This ScalaParser class parses a scala file, extracts the method elements and writes them out to a config file

    """

    #: The regex string specific to scala in order to get the docs, params, returns, type and name.
    regex_string = \
        r"/\*\*([\s,\w,\*,@,\+\.,='\[\]\-/%]*)\*/|(\w+ def|def)\s(\w+)\(([\w+:\s,\[\]=\"\(\)]*)\):\s([\w\[\]]*)"

    def regex_parser(self, data):
        """
        This function takes in data as a string, then uses the regex string variable within this class. To find the
        doc strings, name, parameters, types and return type for each function within the data.
        It then stores this information as a Method class and saves all the methods as a list.
        :param data:
        :return: methods
        """
        # Finds all doc strings, params, names, types, returns types from the data.
        matches = re.finditer(self.regex_string, data, re.MULTILINE)
        methods = []  # Initialising an empty list
        doc_string = ""  # Initialising an empty string
        shorten_doc = [""]
        for match in matches:
            # doc string match separately to the rest of the variables
            # matches look like:
            # ["doc string", None, None, None, None][None, "def", "sum", "df: DataFrame", "DataFrame"] ... ect..
            # This doc string is associated with the following function
            if match.group(2) is None:
                # if the second group is None, then this is a doc string match
                # The full doc string is edited to take out the return type at the bottom if there is one
                doc = re.sub("\n\s.*\*\s@return.*", "", match.group(1))
                # Then the * and white space are taken out, then split by the @ into list
                shorten_doc = re.sub("\n\s*\*?", "", doc).split("@")
                # The first one in the list is the description so this is saved to the doc string variable
                doc_string = shorten_doc[0].strip()
            elif match.group(2) is not None:
                # If the second group is not none then this a function match
                # This gets the function access modifier, protected def, def, private def
                access = match.group(2).replace("def", "").strip()
                if not access:
                    access = "public"

                name = match.group(3)  # This is the name of the function

                # This is the params string -> "df: DataFrame, colA: String"
                # it then gets turn into a parameter list -> ["df:DataFrame", "colA:String"]
                params1 = match.group(4).split(",")
                params = self.parameter_dictionary(params1, shorten_doc[1:])

                return_type = match.group(5)  # Get the return type, if there is nothing it is None
                # Create the method
                method = Method(name, params, str(doc_string), return_type, access, {})
                method.format_name()
                method.format_params()
                # Adds the Method class with the respective variables to the method list
                methods.append(method)
                # doc string is reset to being empty
                doc_string = ""
            else:
                # If no match is found then this is printed out
                print("no match found")
        return methods

    def parameter_dictionary(self, parameter_match, parameter_doc):
        """
        This function takes in two separate lists of strings, one containing the parameters in th following format:
        ["df:DataFrame", 'column:String = "Fred"']
        The other contains the parameter info from the doc string:
        ['@param df DataFrame - Data going in.', '@param column String - column name.']

        These are then looped through with the key points such as name, type, doc and default being picked out.
        It gives you the following dictionary:

        {"df": {"type": "DataFrame", "default": "", "doc": "Data going in."},
         "column": {"type":"String", "default":'"Fred"', "doc":"column name."}
         }

        :param parameter_match: This is a list of strings containing all the parameters
        :type parameter_match: List[Str]
        :param parameter_doc: This is a list of strings containing all the doc parameter info
        :type parameter_doc: List[Str]
        :return:  Dictionary
        """
        # Initialising an empty dictionary
        params = {}
        # {"": {"type": "", "default": "", "doc": ""}}
        wrong_types = [[], [''], None]
        # if there are parameters and a doc string
        if parameter_match not in wrong_types and parameter_doc not in wrong_types:
            for i in range(0, len(parameter_match)):
                default = ""
                name = parameter_match[i].split(":")[0].strip()
                param_type = parameter_match[i].split(":")[1].split("=")
                if len(param_type) > 1:
                    default = param_type[1].strip()

                param_doc_list = parameter_doc[i].split(" ")[3:]
                if param_doc_list == []:
                    param_doc = ""
                elif param_doc_list[0] == "-":
                    param_doc = " ".join(param_doc_list[1:])
                else:
                    param_doc = " ".join(param_doc_list)

                params.update({name: {"type": param_type[0].strip(), "default": default, "doc": param_doc.strip()}})

        elif parameter_match not in wrong_types:
            for i in range(0, len(parameter_match)):
                default = ""
                name = parameter_match[i].split(":")[0].strip()
                param_type = parameter_match[i].split(":")[1].split("=")
                if len(param_type) > 1:
                    default = param_type[1].strip()
                params.update({name: {"type": param_type[0].strip(), "default": default, "doc": ""}})

        return params

    def create_containers(self, methods, file_path):
        """
        This function takes the list of Method classes and a list of file paths, if the file path is empty or none,
        then an error is raised.
        If there are valid file paths then the container name is found using splits on the file path separator and dots.
        From there it checks if there are Method Classes within the method list, if there are then a Container class is
        created and the config is created around that class.
        Otherwise it prints out which container has no methods
        
        :param methods: This is a list of all the methods class within the file.
        :type methods: List[str]
        :param file_path: This is the file path to the file currently being parsed.
        :type file_path: str
        """
        invalid_files = [None, ""]
        if file_path not in invalid_files:
            # this gets the file's name as the container name
            container_name = os.path.normpath(file_path).split(str(os.sep))[-1].split(".")[0]
            if methods:
                container = Container(container_name, methods, file_path)
                container.format_name()
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

        print("finished for loop")
        print(self.containers)
        if self.containers:
            self.write_config()
        else:
            message = "Config string is empty"
            print("Container list: ", self.containers)
            raise Exception(message)
