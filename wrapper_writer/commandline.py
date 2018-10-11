import argparse

from wrapper_writer.parsers import ScalaParse
from wrapper_writer.wrapper_writer import WrapperWriter


def get_args():
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
    parser_wrap.add_argument('-m', '--method-config', default='./method_config.yml',
                             help='The path to the method config file')
    parser_wrap.add_argument('-s', '--structure-config', default='./structure_config.yml',
                             help='The path to the structure config file')

    # Create the parser for the Parser
    parser_parse = subparsers.add_parser('parse', help='Create a configuration by parsing existing files')
    parser_parse.set_defaults(command='parse')
    parser_parse.add_argument('-c', '--config-name', default='method_config.yml',
                              help="The name of the config file to write to")
    parser_parse.add_argument('-a', '--append-config', default="w",
                              help='a: Append an existing config file, w: Overwrite if config file exists')
    parser_parse.add_argument('-f', '--files', default=None,
                              help='A comma separated list of absolute file paths to be parsed')
    parser_parse.add_argument('-d', '--directory', default=None,
                              help='The absolute path to a directory containing files to be parsed')
    parser_parse.add_argument('-t', '--target-format', default=".*\.scala",
                              help='The format of the files to read from the directory')

    # Parse the argument lists
    return parser.parse_args()


def parse(args):
    """
    This method validates the arguments and calls the ScalaParser class.

    :param args: A object containing the commandline arguments.
    :type args: argparse.Namespace
    :return:
    """
    # Check args

    # Parse
    p = ScalaParse(args.config_name, args.append_config)
    if args.files:
        p.files.extend(args.files.split(","))
    if args.directory:
        p.get_files(args.directory, args.target_format)

    p.multi_process()

    p.write_config()


def wrap(args):
    """
    This method validates the arguments and calls the Wrapper class.

    :param args: A object containing the commandline arguments.
    :type args: argparse.Namespace
    :return:
    """
    # Check args
    # The appropriate errors are raised by the method

    # Wrap
    WrapperWriter(args.method_config, args.structure_config).run()


def commandline():
    """
    This function allows us to use the command line to call either the parse methods or the wrap methods.

    :return:
    """
    args = get_args()

    # Parse
    if args.command == "parse":
        parse(args)

    # Wrap
    elif args.command == "wrap":
        wrap(args)
