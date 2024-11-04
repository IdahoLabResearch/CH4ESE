""""
CH4ESE - Conversion Helper 4 Easy Serialization of EXI
Copyright 2024, Battelle Energy Alliance, LLC
"""

from argparse import ArgumentParser
from time import time
import sys
import xml.dom.minidom
from connection.connect import create_gateway
from exi_conversions.conversions import decode_exi, encode_xml
from grammar import create_grammar
from profiles.profiles import profiles
from server.multi_threaded_server import run
import log


def process_input(args):
    """Processes the user's input arguments"""
    data_input = None

    if args.i is None:
        data_input = args.s
    else:
        with open(args.i, "r", encoding="utf-8") as input_file:
            data_input = input_file.read()

    # if it is an EXI message, removes any white spaces
    if args.d:
        data_input = data_input.replace(" ", "")

    return data_input


def validate_profile(profile_arg):
    """Verifies that the user-provided profile has been defined"""
    if profile_arg in profiles.keys():
        return
    log.logger.error(f"The provided profile name does not exist: {profile_arg}")
    sys.exit()


def main():
    result: str

    parser = ArgumentParser(
        prog="python3 main.py",
        description="This tool is used to perform EXI conversions",
    )

    input_group = parser.add_argument_group("Input Options")
    input_group = input_group.add_mutually_exclusive_group()
    input_group.add_argument("-i", metavar="<Path to input file>", help="Path to the input file")
    input_group.add_argument("-s", metavar="<EXI/XML string>", help="A string input")

    output_group = parser.add_argument_group("Output Options", "Defaults to console output")
    output_group.add_argument("-o", metavar="<Output file>", help="Path to the output file")

    mode_group = parser.add_argument_group("Mode Options")
    mode_group = mode_group.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("-e", action="store_true", help="Toggle XML encoding mode")
    mode_group.add_argument("-d", action="store_true", help="Toggle EXI decoding mode")
    mode_group.add_argument("-w", action="store_true", help="Enable the web server")

    config_options = parser.add_argument_group("Configuration Options")
    config_options.add_argument(
        "-profile",
        metavar="<Profile Name>",
        help="Name of the schema profile",
        required=True,
    )
    config_options.add_argument(
        "-p",
        metavar="port_number",
        type=int,
        default=8080,
        help="Port for the webserver to run on. Default: 8080",
    )
    config_options.add_argument("-v", action="store_true", help="Verbose mode")

    # process command-line arguments
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit("No arguments provided")
    args = parser.parse_args()
    log.create_logger(args.v)
    data_input = process_input(args)
    validate_profile(args.profile)
    log.logger.info("Arguments Processed Successfully.")

    # connects to the .jar file and creates the grammar factory for validation of the connection
    gateway, grammar_factory = create_gateway()

    # creates the schema-informed grammars for encoding/decoding
    profile = create_grammar(grammar_factory, profiles[args.profile])

    start = time()

    if args.e:
        log.logger.info("Encoding XML...")
        result = encode_xml(str(data_input), profile, gateway)
    elif args.d:
        log.logger.info("Decoding EXI message...")
        result = decode_exi(bytes.fromhex(data_input), profile, gateway)
    elif args.w:
        log.logger.info("Initializing Web Server...")
        run(args.p, profile, gateway)

    conv_time = time() - start
    log.logger.info(f"Conversion Time: {conv_time}\n")

    if args.o is None:
        print(result)
    else:
        with open(args.o, "w", encoding="utf-8") as output_file:
            if args.d:
                xml_data = xml.dom.minidom.parseString(result)
                output_file.write(xml_data.toprettyxml())
            else:
                output_file.write(result)


if __name__ == "__main__":
    main()
