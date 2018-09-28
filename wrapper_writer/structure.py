import os

class Structure:
    full_path = ""

    def __init__(self, path, template, file_name_format):
        self.path = path
        self.template = template
        self.file_name_format = file_name_format

    def create_path(self):
        """
        This function combines the given path (relative path) with the current working directory to get the absolute path
        :return:
        """
        self.full_path = os.getcwd()+ self.path


    def create_dir(self):
        """
        This function makes directories from the full path variable. If the directory already exist then this will
        catch the error and print which directory exists.
        """
        try:
            # creating the directories
            os.makedirs(self.full_path)
        except FileExistsError:
            # if directory exist then the error is caught
            print(self.full_path + " already exists")


