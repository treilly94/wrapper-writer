import argparse
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

# Parse the argument lists
args = parser.parse_args()


def commandline():

    if args.command == "parse":
        print("Parsing ...")

    elif args.command == "wrap":
        WrapperWriter(args.method_config, args.structure_config).run()


if __name__ == "__main__":
    commandline()
