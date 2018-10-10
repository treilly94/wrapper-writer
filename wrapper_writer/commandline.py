import argparse

from wrapper_writer.scala_parser import ScalaParse
from wrapper_writer.wrapper_writer import WrapperWriter

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
parser_parse.add_argument('-a', '--append-config', default=False,
                          help='True: Append an existing config file, False: Overwrite if config file exists')
parser_parse.add_argument('-f', '--files', default=None,
                          help='A comma separated list of absolute file paths to be parsed')
parser_parse.add_argument('-d', '--directory', default=None,
                          help='The absolute path to a directory containing files to be parsed')
parser_parse.add_argument('-t', '--target-format', default=".*\.scala",
                          help='The format of the files to read from the directory')

# Parse the argument lists
args = parser.parse_args()


def commandline():
    # Parse
    if args.command == "parse":
        p = ScalaParse(args.config_name, args.append_config)
        if args.files:
            p.files.extend(args.files.split(","))
        if args.directory:
            p.get_files(args.directory, args.target_format)

        p.multi_process()

        p.write_config()

    # Wrap
    elif args.command == "wrap":
        WrapperWriter(args.method_config, args.structure_config).run()


if __name__ == "__main__":
    commandline()
