#!/usr/bin/env python3

import sys
import logging
import argparse
from expert_system.parser.parser import Parser
from expert_system.inference_engine.inference_engine import InferenceEngine


def check_python_version():
    assert sys.version_info >= (3, 0)


def argument_parser():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("file")

    arg_parser.add_argument("-v", "--verbose", help="Prints logic visualisation", action="store_true")
    arg_parser.add_argument("-g", "--graphic", help="Displays graph in a separate window", action="store_true")
    arg_parser.add_argument("-i", "--interactive", help="Interactive fact validation", action="store_true")

    return arg_parser.parse_args()


def configure_verbose_logging(is_verbose):
    logging_format = "%(message)s"

    if is_verbose:
        logging.basicConfig(level=logging.DEBUG, format=logging_format)
    else:
        logging.basicConfig(level=logging.INFO, format=logging_format)


if __name__ == "__main__":
    check_python_version()
    parsed_args = argument_parser()

    configure_verbose_logging(parsed_args.verbose)

    parser = Parser(parsed_args.file)

    parser.tokenize_file()

    engine = InferenceEngine(verbose=parsed_args.verbose,
                             graphic=parsed_args.graphic,
                             interactive=parsed_args.interactive,
                             queries=parser.queries,
                             initial_facts=parser.initial_facts,
                             rules=parser.rules)

    engine.resolve_queries()

