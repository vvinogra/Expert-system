import lexeme
from lexer_exception import LexerException
import networkx as nx


class Lexer:

    def __init__(self, filename):
        self._filename = filename

        self._parsed_initial_facts = False
        self._parsed_queries = False
        self._true_initial_facts = []
        self._queries = []

        self._graph = nx.DiGraph()
        # self._graph.add_node(1)
        # self._graph.add_edge(1, 2)
        # print(self._graph)

    def tokenize_file(self):
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
                    rule = self._tokenize_rule(line)

                    parsed_rule = self._parse_rule(rule)

                # split_line = line.split()

                # if len(split_line) == 1:
                #     first_elem = split_line[0]
                #
                #     if first_elem.startswith("="):
                #         self._check_for_initial_facts(first_elem)
                #     elif first_elem.startswith("?"):
                #         self._check_for_queries(first_elem)
                # elif len(split_line) > 1:
                #     rule = self._tokenize_rule(line)
                #
                #     parsed_rule = self._parse_rule(rule)

                    # for i in rule:
                    #     print(i.value)
                    # self._add_rule_to_graph(split_line)




                            # if elem in type_value:
                            #     print(elem)
                            #     break
                            # else:
                            #     print("Error! Elem = " + elem)


                # for lexeme_type, type_value in lexeme.LEXEME_TYPES.items():
                #     if type_value

                # print(split_line)
                pass

        # print(self._queries)
        # print(self._true_initial_facts)

    def _check_for_initial_facts(self, facts):
        if self._parsed_initial_facts:
            raise LexerException("Initial facts line occurred twice")

        for fact in facts[1:]:
            if fact in lexeme.LEXEME_TYPES["FACT"]:
                self._true_initial_facts.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["FACT"], fact))
            else:
                raise LexerException("Invalid fact in initial facts")

        self._parsed_initial_facts = True

    def _check_for_queries(self, queries):
        if self._parsed_queries:
            raise LexerException("Line with queries occurred twice")

        if len(queries) == 1:
            raise LexerException("No queries are specified")

        for query in queries[1:]:
            if query in lexeme.LEXEME_TYPES["FACT"]:
                self._queries.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["FACT"], query))
            else:
                raise LexerException("Invalid fact in queries")

        self._parsed_queries = True

    def _add_rule_to_graph(self, rule):
        # rule
        pass

    def _tokenize_rule(self, line):
        lexeme_list = []
        chars_to_skip = 0

        for i in range(len(line)):
            if chars_to_skip:
                chars_to_skip -= 1
                continue
            elif line[i].isspace():
                continue
            elif line[i] in lexeme.LEXEME_TYPES["FACT"]:
                lexeme_list.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["FACT"], line[i]))
            else:
                cut_line = line[i:]
                operand_found = False

                for l_type, l_value in lexeme.LEXEME_SYMBOLS.items():
                    if cut_line.startswith(l_value):
                        lexeme_list.append(lexeme.Lexeme(l_type, l_value))
                        chars_to_skip = len(l_value) - 1
                        operand_found = True

                if not operand_found:
                    raise LexerException("Invalid operator")

        return lexeme_list

    def _parse_rule(self, rule):
        left_side = []
        right_side = []
        conclusion_op = None

        for token in rule:
            if token.type in lexeme.LEXEME_EQUATION_OPERANDS.keys():
                if not conclusion_op:
                    conclusion_op = token
                else:
                    raise LexerException("Multiple conclusion operands")
            else:
                if not conclusion_op:
                    left_side.append(token)
                else:
                    right_side.append(token)

        if not conclusion_op:
            raise LexerException("No conclusion operand")

        if not len(left_side):
            raise LexerException("Equation part is empty")

        if not len(right_side):
            raise LexerException("Conclusion part is empty")

        return left_side, conclusion_op, right_side

        # for i in range(len(rule)):
        #     if rule[i].isspace():
        #         continue
        #     elif rule[i] in lexeme.LEXEME_TYPES["FACT"]:
        #         output.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["FACT"], rule[i]))
        #     elif rule[i] == lexeme.LEXEME_TYPES["OP_NOT"]:
        #         stack.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["OP_NOT"], rule[i]))
        #     elif rule[i] == lexeme.LEXEME_TYPES["LEFT_BRACE"]:
        #         stack.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["LEFT_BRACE"], rule[i]))
        #     elif rule[i] == lexeme.LEXEME_TYPES["RIGHT_BRACE"]:
        #         pass
        #
        #         # lexemes_list.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["RIGHT_BRACE"], rule[i]))
        #     else:
        #         cut_line = rule[i:]
        #         # operand_found = False
        #
        #         for l_type, l_value in lexeme.LEXEME_INFIX_OPERANDS.items():
        #             if cut_line.startswith(l_value):
        #                 stack.append(lexeme.Lexeme(l_type, l_value))
                        # chars_to_skip = len(l_value) - 1
                        # value_operands_count -= 1
                        # operand_found = True

                # if not operand_found:
                #     raise LexerException("Invalid operator")

    # def _create_rule(self, line):
    #     # lexemes_list = []
    #
    #     stack = []
    #     output = []
    #
    #     for i in range(len(line)):
    #         if line[i].isspace():
    #             continue
    #         elif line[i] in lexeme.LEXEME_TYPES["FACT"]:
    #             output.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["FACT"], line[i]))
    #         elif line[i] == lexeme.LEXEME_TYPES["OP_NOT"]:
    #             stack.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["OP_NOT"], line[i]))
    #         elif line[i] == lexeme.LEXEME_TYPES["LEFT_BRACE"]:
    #             stack.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["LEFT_BRACE"], line[i]))
    #         elif line[i] == lexeme.LEXEME_TYPES["RIGHT_BRACE"]:
    #             pass
    #
    #             # lexemes_list.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["RIGHT_BRACE"], line[i]))
    #         else:
    #             cut_line = line[i:]
    #             # operand_found = False
    #
    #             for l_type, l_value in lexeme.LEXEME_INFIX_OPERANDS.items():
    #                 if cut_line.startswith(l_value):
    #                     stack.append(lexeme.Lexeme(l_type, l_value))
    #                     # chars_to_skip = len(l_value) - 1
    #                     # value_operands_count -= 1
    #                     # operand_found = True
    #
    #             # if not operand_found:
    #             #     raise LexerException("Invalid operator")
    #
    #     # if braces_count:
    #     #     raise LexerException("Invalid braces count")
    #     #
    #     # if value_operands_count != 1:
    #     #     raise LexerException("Invalid rule")
    #
    #     # return lexemes_list

    # def _create_rule(self, line):
    #     lexemes_list = []
    #
    #     chars_to_skip = 0
    #     value_operands_count = 0
    #     braces_count = 0
    #
    #     for i in range(len(line)):
    #         if chars_to_skip:
    #             chars_to_skip -= 1
    #             continue
    #         elif line[i].isspace():
    #             continue
    #         elif line[i] in lexeme.LEXEME_TYPES["FACT"]:
    #             lexemes_list.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["FACT"], line[i]))
    #             value_operands_count += 1
    #         elif line[i] == lexeme.LEXEME_TYPES["OP_NOT"]:
    #             lexemes_list.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["OP_NOT"], line[i]))
    #
    #             cut_line = line[i + len(lexeme.LEXEME_TYPES["OP_NOT"]):]
    #
    #             if not (cut_line.startswith(lexeme.LEXEME_TYPES["FACT"]) or
    #                     cut_line.startswith(lexeme.LEXEME_TYPES["LEFT_BRACE"]) or
    #                     cut_line.startswith(lexeme.LEXEME_TYPES["OP_NOT"])):
    #                 raise LexerException("Invalid value after negation operator")
    #
    #         elif line[i] == lexeme.LEXEME_TYPES["LEFT_BRACE"]:
    #             lexemes_list.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["LEFT_BRACE"], line[i]))
    #             braces_count += 1
    #         elif line[i] == lexeme.LEXEME_TYPES["RIGHT_BRACE"]:
    #             lexemes_list.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["RIGHT_BRACE"], line[i]))
    #             braces_count -= 1
    #         else:
    #             cut_line = line[i:]
    #             operand_found = False
    #
    #             for l_type, l_value in lexeme.LEXEME_VALUE_OPERANDS.items():
    #                 if cut_line.startswith(l_value):
    #                     lexemes_list.append(lexeme.Lexeme(l_type, l_value))
    #                     chars_to_skip = len(l_value) - 1
    #                     value_operands_count -= 1
    #                     operand_found = True
    #
    #             if not operand_found:
    #                 raise LexerException("Invalid operator")
    #
    #     if braces_count:
    #         raise LexerException("Invalid braces count")
    #
    #     if value_operands_count != 1:
    #         raise LexerException("Invalid rule")
    #
    #     return lexemes_list
