import logging
from cmd import Cmd

from expert_system.inference_engine.inference_engine import InferenceEngine
from expert_system.inference_engine.inference_engine import InferenceEngineException

from expert_system.parser.parser import Parser
from expert_system.parser.parser_exception import ParserException


class InferenceEngineShell(Cmd):
    intro = "Welcome to the Inference Engine shell.\n" \
            "Type help or ? to list commands."
    prompt = "(engine) "
    parser = None
    verbose_mode = False

    def do_parse(self, filename):
        """Parse new file: parse filename"""
        if not filename:
            logging.info("Please enter the filename")
            return

        try:
            self.parser = Parser(filename)

            self.parser.tokenize_file()
        except ParserException as e:
            self.parser = None
            logging.error("\033[31m" + "PARSER ERROR: {}".format(str(e)) + "\033[0m")  # Red colored

    def do_facts(self, new_initial_facts):
        """Print or set initial facts: facts [new initial facts]"""
        if not self.parser:
            logging.warning("Parsed file is not valid")
            return

        if new_initial_facts:
            backup_initial_facts = self.parser.initial_facts

            self.parser.initial_facts = []

            try:
                self.parser.parse_initial_facts(new_initial_facts)
            except ParserException as e:
                self.parser.initial_facts = backup_initial_facts
                logging.error("\033[31m" + "PARSER ERROR: {}".format(str(e)) + "\033[0m")  # Red colored
        else:
            logging.info(self.parser.initial_facts)

    def do_queries(self, new_queries):
        """Print or set queries: queries [new queries]"""
        if not self.parser:
            logging.warning("Parsed file is not valid")
            return

        if new_queries:
            backup_queries = self.parser.queries

            self.parser.queries = []

            try:
                self.parser.parse_queries(new_queries)
            except ParserException as e:
                self.parser.queries = backup_queries
                logging.error("\033[31m" + "PARSER ERROR: {}".format(str(e)) + "\033[0m")  # Red colored
        else:
            logging.info(self.parser.queries)

    def do_verbose(self, status):
        """Print or set verbose mode: verbose [True/False]"""
        if type(status) is bool:
            self.verbose_mode = status
        else:
            if not status:
                logging.info(self.verbose_mode)
            else:
                if status == "True":
                    self.verbose_mode = True
                elif status == "False":
                    self.verbose_mode = False
                else:
                    logging.warning("Invalid verbose mode status")

    def do_exec(self, arg):
        """Resolve undefined queries: exec"""
        if arg:
            logging.warning("\"exec\" command doesn't accept any arguments")
            return

        if not self.parser:
            logging.warning("Parsed file is not valid")
            return

        try:
            engine = InferenceEngine(verbose=self.verbose_mode,
                                     graphic=False,
                                     queries=self.parser.queries,
                                     initial_facts=self.parser.initial_facts,
                                     rules=self.parser.rules)

            engine.resolve_queries()
        except InferenceEngineException as e:
            logging.error("\033[31m" + "RUNTIME ERROR: {}".format(str(e)) + "\033[0m")  # Red colored

    def do_EOF(self, line):
        return True

    def do_exit(self, line):
        """Exits program"""
        return True

    def emptyline(self):
        pass
