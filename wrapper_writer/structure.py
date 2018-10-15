import os


class Structure:
    """The Structure Class contains the details and functionality associated with a particular structure.

    .. note:: A structure is a group of wrappers that would use the same template, follow the same naming convention, and be placed in the same directory.

    :param project_root: This is the absolute path to the project
    :type project_root: str
    :param path: The relative path from the project root where the new files will be placed.
    :type path: str
    :param template: The name of the template file to use.
    :type template: str
    :param file_name_format: The format of the new file names using PyFormat where a {} represents the file name.
    :type file_name_format: str
    :param access: A list of the access modifiers to be written
    :type access: list[str]
    """

    full_path = ""  #: This is the full path from the starting drive to the directory in question.

    def __init__(self, project_root, path, template, file_name_format, access=["public"]):
        self.project_root = os.path.normpath(project_root)
        self.path = os.path.normpath(path)
        self.template = template
        self.file_name_format = file_name_format
        self.access = access

    def create_path(self):
        """This function combines the given path (relative path) with the current working directory to get the
        absolute path

        :return: None
        """

        self.full_path = os.path.join(self.project_root, self.path)

    def create_dir(self):
        """This function makes directories from the full path variable. If the directory already exist then this will
        catch the error and print which directory exists.

        :return: None
        """
        try:
            # creating the directories
            os.makedirs(self.full_path)
        except FileExistsError:
            # if directory exist then the error is caught
            print(self.full_path + " already exists")
