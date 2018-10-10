import argparse
from wrapper_writer.wrapper_writer import WrapperWriter
from wrapper_writer.scala_parser import Parser, ScalaParse

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
parser_parse.add_argument('-f', '--scala-folder', default=None,
                         help='The folder path where code to be parsed lives')
parser_parse.add_argument('-l', '--logic-file', default=None,
                          help='The file path, where code to be parsed lives')
parser_parse.add_argument('-a', '--append-config', default=False,
                          help='True: Append an existing config file, False: Overwrite if config file exists')
parser_parse.add_argument('-c', '--config-name', default='./')

# Parse the argument lists
args = parser.parse_args()
# folder=None, logic_file=None, target_format="*.scala", config_name="config_sadhg.yml", append_config=False

def commandline():

    if args.command == "parse":
        print("Parsing ...")
        Parser()


    elif args.command == "wrap":
        WrapperWriter(args.method_config, args.structure_config).run()


if __name__ == "__main__":
    commandline()
