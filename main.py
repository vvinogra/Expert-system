#!/usr/bin/env python3

import sys
import logging
import argparse
from expert_system.parser.parser import Parser
from expert_system.parser.parser import ParserException
from expert_system.inference_engine.inference_engine import InferenceEngine
from expert_system.inference_engine.inference_engine import InferenceEngineException
from expert_system.shell.inference_engine_shell import InferenceEngineShell


def check_python_version():
    assert sys.version_info >= (3, 0)


def argument_parser():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("filename", help="input filename")

    arg_parser.add_argument("-v", "--verbose", help="print logic visualisation", action="store_true", default=False)
    arg_parser.add_argument("-g", "--graphic", help="display graph in a separate window", action="store_true", default=False)
    arg_parser.add_argument("-i", "--interactive", help="interactive fact validation", action="store_true", default=False)

    return arg_parser.parse_args()


def configure_logging():
    logging_format = "%(message)s"

    logging.basicConfig(level=logging.INFO, format=logging_format)


if __name__ == "__main__":
    check_python_version()
    parsed_args = argument_parser()

    configure_logging()

    if parsed_args.interactive:
        if parsed_args.graphic:
            logging.error("Can't run graphic and interactive modes together")
            sys.exit(0)

        shell = InferenceEngineShell()

        shell.do_verbose(parsed_args.verbose)
        shell.do_parse(parsed_args.filename)
        shell.cmdloop()
    else:
        if parsed_args.verbose:
            logging.info("\33[32m" + "STARTING!" + "\033[0m")  # Green colored

        try:
            parser = Parser(parsed_args.filename)

            parser.tokenize_file()

            engine = InferenceEngine(verbose=parsed_args.verbose,
                                     queries=parser.queries,
                                     initial_facts=parser.initial_facts,
                                     rules=parser.rules)

            engine.resolve_queries()

            engine.print_queries()

            if parsed_args.graphic:
                engine.show_graph_plot()
        except InferenceEngineException as e:
            logging.error("\033[31m" + "RUNTIME ERROR: {}".format(str(e)) + "\033[0m")  # Red colored
        except ParserException as e:
            logging.error("\033[31m" + "PARSER ERROR: {}".format(str(e)) + "\033[0m")  # Red colored

        if parsed_args.verbose:
            logging.info("\33[32m" + "EXITING..." + "\033[0m")  # Green colored
