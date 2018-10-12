import argparse
import os
import sys

from wrapper_writer.parsers import ScalaParse
from wrapper_writer.wrapper_writer import WrapperWriter


def existing_files(string):
    """
    This method checks that the provided file(s) exists and if not raises an error.

    :param string: The file path(s)
    :type string: str
    :return: str
    """
    split_string = string.split(",")

    for i in split_string:
        if not os.path.isfile(i):
            raise argparse.ArgumentTypeError(i + " cant be found, does it exist?")

    return string


def existing_directory(string):
    """
    This method checks that the provided directory exists and if not raises an error.

    :param string: The directory
    :type string: str
    :return: str
    """
    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError(string + " cant be found, does it exist?")

    return string


def valid_write_option(string):
    """
    This method checks whether the string is one of the valid write options and if not raises an error.

    :param string: The write option
    :type string: str
    :return: str
    """
    valid_options = ["w", "a"]

    if string not in valid_options:
        raise argparse.ArgumentTypeError(string + " isn't a valid write option. Must be either w or a")

    return string


def get_args(args):
    """
    This method uses argparse to get the commandline arguments.

    :return: argparse.Namespace
    """
    # Create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Create the parser for the Wrapper
    parser_wrap = subparsers.add_parser('wrap', help='Create the wrappers')
    parser_wrap.set_defaults(command='wrap')
    parser_wrap.add_argument('-m', '--method-config', type=existing_files, default='./method_config.yml',
                             help='The path to the method config file')
    parser_wrap.add_argument('-s', '--structure-config', type=existing_files, default='./structure_config.yml',
                             help='The path to the structure config file')

    # Create the parser for the Parser
    parser_parse = subparsers.add_parser('parse', help='Create a configuration by parsing existing files')
    parser_parse.set_defaults(command='parse')
    parser_parse.add_argument('-c', '--config-name', default='method_config.yml',
                              help="The name of the config file to write to")
    parser_parse.add_argument('-a', '--append-config', type=valid_write_option, default="w",
                              help='a: Append an existing config file, w: Overwrite if config file exists')
    parser_parse.add_argument('-f', '--files', type=existing_files, default=None,
                              help='A comma separated list of absolute file paths to be parsed')
    parser_parse.add_argument('-d', '--directory', type=existing_directory, default=None,
                              help='The absolute path to a directory containing files to be parsed')
    parser_parse.add_argument('-t', '--target-format', default=".*\.scala",
                              help='The format of the files to read from the directory')

    # Parse the argument lists
    return parser.parse_args(args)


def parse(args):
    """
    This method validates the arguments and calls the ScalaParser class.

    :param args: A object containing the commandline arguments.
    :type args: argparse.Namespace
    :return:
    """
    p = ScalaParse(args.config_name, args.append_config)
    if args.files:
        p.files.extend(args.files.split(","))
    if args.directory:
        p.get_files(args.directory, args.target_format)

    p.run()


def wrap(args):
    """
    This method validates the arguments and calls the Wrapper class.

    :param args: A object containing the commandline arguments.
    :type args: argparse.Namespace
    :return:
    """
    WrapperWriter(args.method_config, args.structure_config).run()


def commandline():
    """
    This function allows us to use the command line to call either the parse methods or the wrap methods.

    :return:
    """
    args = get_args(sys.argv[1:])

    # Parse
    if args.command == "parse":
        parse(args)

    # Wrap
    elif args.command == "wrap":
        wrap(args)
