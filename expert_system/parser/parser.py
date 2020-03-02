from .parser_exception import ParserException
from expert_system.common.lexeme_types import LexemeTypes
from expert_system.common.fact import Fact

from expert_system.common.operator import OperatorFactory, ConclusionOperator
from expert_system.common.rule import Rule


class Parser:

    def __init__(self, filename):
        self._filename = filename

        self._parsed_initial_facts = False
        self._parsed_queries = False
        self.initial_facts = []
        self.queries = []
        self.rules = []

    def tokenize_file(self):
        try:
            with open(self._filename, "r") as file:
                for line in file:
                    # Removing comment
                    line = line.partition("#")[0]

                    # Removing trailing whitespaces
                    line = line.strip()

                    if not len(line):
                        continue

                    if line[0].startswith("="):
                        self._check_for_initial_facts(line)
                    elif line[0].startswith("?"):
                        self._check_for_queries(line)
                    else:
                        self._parse_rule(line)

            self._check_for_input_values_definition()
        except IOError as e:
            raise ParserException(str(e))

    def _check_for_initial_facts(self, facts):
        if self._parsed_initial_facts:
            raise ParserException("Initial facts line occurred twice")

        for fact in facts[1:]:
            if fact in LexemeTypes.FACT:
                self.initial_facts.append(Fact(fact))
            else:
                raise ParserException("Invalid fact in initial facts")

        self._parsed_initial_facts = True

    def _check_for_queries(self, queries):
        if self._parsed_queries:
            raise ParserException("Line with queries occurred twice")

        if len(queries) == 1:
            raise ParserException("No queries are specified")

        for query in queries[1:]:
            if query in LexemeTypes.FACT:
                self.queries.append(Fact(query))
            else:
                raise ParserException("Invalid fact in queries")

        self._parsed_queries = True

    def _check_for_input_values_definition(self):
        if not self._parsed_queries:
            raise ParserException("Queries are not defined")

        if not self._parsed_initial_facts:
            raise ParserException("Initial facts are not defined")

    def _tokenize_rule(self, line):
        token_list = []
        chars_to_skip = 0

        for i in range(len(line)):
            if chars_to_skip:
                chars_to_skip -= 1
                continue
            elif line[i].isspace():
                continue
            elif line[i] in LexemeTypes.FACT:
                token_list.append(Fact(line[i]))
            else:
                cut_line = line[i:]
                operand_found = False

                for op in OperatorFactory.operators_list:
                    if cut_line.startswith(op):
                        token_list.append(OperatorFactory.get_operator(op))
                        chars_to_skip = len(op) - 1
                        operand_found = True

                if not operand_found:
                    raise ParserException("Invalid operator")

        return token_list

    def _partition_rule(self, rule):
        left_side = []
        right_side = []
        conclusion_op = None

        for token in rule:
            if type(token) is ConclusionOperator:
                if not conclusion_op:
                    conclusion_op = token
                else:
                    raise ParserException("Multiple conclusion operands")
            else:
                if not conclusion_op:
                    left_side.append(token)
                else:
                    right_side.append(token)

        if not conclusion_op:
            raise ParserException("No conclusion operand")

        if not len(left_side):
            raise ParserException("Equation part is empty")

        if not len(right_side):
            raise ParserException("Conclusion part is empty")

        return left_side, conclusion_op, right_side

    def _parse_rule(self, rule):
        tokenized_rule = self._tokenize_rule(rule)

        left_side, conclusion_op, right_side = self._partition_rule(tokenized_rule)

        rule_node = Rule(left_side, conclusion_op, right_side)

        self.rules.append(rule_node)
