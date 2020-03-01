#!/usr/bin/env python3

import sys
import logging
import argparse
from expert_system.parser.parser import Parser
from expert_system.parser.parser import ParserException
from expert_system.inference_engine.inference_engine import InferenceEngine
from expert_system.inference_engine.inference_engine import InferenceEngineException


def check_python_version():
    assert sys.version_info >= (3, 0)


def argument_parser():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("file")

    arg_parser.add_argument("-v", "--verbose", help="Prints logic visualisation", action="store_true")
    arg_parser.add_argument("-g", "--graphic", help="Displays graph in a separate window", action="store_true")
    arg_parser.add_argument("-i", "--interactive", help="Interactive fact validation", action="store_true")

    return arg_parser.parse_args()


def configure_logging():
    logging_format = "%(message)s"

    logging.basicConfig(level=logging.INFO, format=logging_format)


if __name__ == "__main__":
    check_python_version()
    parsed_args = argument_parser()

    configure_logging()

    if parsed_args.verbose:
        logging.info("\33[32m" + "STARTING!" + "\033[0m")

    try:
        parser = Parser(parsed_args.file)

        parser.tokenize_file()

        engine = InferenceEngine(verbose=parsed_args.verbose,
                                 graphic=parsed_args.graphic,
                                 interactive=parsed_args.interactive,
                                 queries=parser.queries,
                                 initial_facts=parser.initial_facts,
                                 rules=parser.rules)

        engine.resolve_queries()
    except InferenceEngineException as e:
        logging.error("\033[31m" + "RUNTIME ERROR: {}".format(str(e)) + "\033[0m")
    except ParserException as e:
        logging.error("\033[31m" + "PARSER ERROR: {}".format(str(e)) + "\033[0m")

    if parsed_args.verbose:
        logging.info("\33[32m" + "EXITING..." + "\033[0m")
