from lexer_exception import LexerException
from lexeme import *
import networkx as nx
import matplotlib.pyplot as plt


class Lexer:

    def __init__(self, filename):
        self._filename = filename

        self._parsed_initial_facts = False
        self._parsed_queries = False
        self._true_initial_facts = []
        self._queries = []

        self._graph = nx.MultiDiGraph()
        # self._graph.add_node(1)
        # self._graph.add_edge(1, 2)
        # print(self._graph.nodes)

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

                    # partitioned_rule = self._partition_rule(rule)

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

        # for i in self._graph.nodes:
        #     print("i.name = {}; i._rule_queries = {}".format(i.name, i._rule_queries))

        nx.draw(self._graph,
                with_labels=True,
                arrows=True,
                pos=nx.circular_layout(self._graph))

        # nx.drawing.nx_pydot.write_dot(self._graph, "test.png")

        # edge_labels = nx.get_edge_attributes(self._graph, 'rule')
        #
        # for a,b,c in edge_labels:
        #     print(a, b, c)

        # edge_labels = self._graph.edges.data(True)

        # print(edge_labels)

        # edge_labels = dict([((u, v,), d['rule'])
        #                     for u, v, d in self._graph.edges(data=True)])
        #
        # nx.draw_networkx_edge_labels(self._graph,
        #                              nx.circular_layout(self._graph),
        #                              edge_labels=edge_labels,
        #                              rotate=True,
        #                              font_size=6)

        # nx.draw_networkx_edges(self._graph,
        #                        with_labels=True,
        #                        arrows=True,
        #                        pos=nx.circular_layout(self._graph),
        #                        node_size=100)
        plt.show()
        # print(self._queries)
        # print(self._true_initial_facts)

    def _check_for_initial_facts(self, facts):
        if self._parsed_initial_facts:
            raise LexerException("Initial facts line occurred twice")

        for fact in facts[1:]:
            if fact in LexemeTypes.FACT.value:
                self._true_initial_facts.append(Lexeme(LexemeTypes.FACT, fact))
            else:
                raise LexerException("Invalid fact in initial facts")

        self._parsed_initial_facts = True

    def _check_for_queries(self, queries):
        if self._parsed_queries:
            raise LexerException("Line with queries occurred twice")

        if len(queries) == 1:
            raise LexerException("No queries are specified")

        for query in queries[1:]:
            if query in LexemeTypes.FACT.value:
                self._queries.append(Lexeme(LexemeTypes.FACT, query))
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
            elif line[i] in LexemeTypes.FACT.value:
                lexeme_list.append(Lexeme(LexemeTypes.FACT, line[i]))
            else:
                cut_line = line[i:]
                operand_found = False

                for l_type in LEXEME_SYMBOLS:
                    if cut_line.startswith(l_type.value):
                        lexeme_list.append(Lexeme(l_type, l_type.value))
                        chars_to_skip = len(l_type.value) - 1
                        operand_found = True

                if not operand_found:
                    raise LexerException("Invalid operator")

        return lexeme_list

    def _partition_rule(self, rule):
        left_side = []
        right_side = []
        conclusion_op = None

        for token in rule:
            if token.type in LEXEME_IMPLICATION_TYPES:
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

    def _convert_to_rpl(self, token_list):
        output = []
        stack = []
        expect_operand = True

        for token in token_list:
            if token.type == LexemeTypes.FACT:
                if not expect_operand:
                    raise LexerException("Expecting operator")

                expect_operand = False

                output.append(token)
            elif token.type in LEXEME_PREFIX_OPERANDS:
                if not expect_operand:
                    raise LexerException("Expecting operand")

                expect_operand = True

                stack.append(token)
            elif token.type == LexemeTypes.LEFT_BRACKET:
                if not expect_operand:
                    raise LexerException("Expecting operand")

                expect_operand = True

                stack.append(token)
            elif token.type == LexemeTypes.RIGHT_BRACKET:
                if expect_operand:
                    raise LexerException("Expecting operand")

                expect_operand = False

                while stack:
                    last_token = stack.pop()

                    if last_token.type == LexemeTypes.LEFT_BRACKET:
                        break

                    output.append(last_token)

                if not stack:
                    raise LexerException("Invalid brackets count")

            elif token.type in LEXEME_INFIX_OPERANDS:
                if expect_operand:
                    raise LexerException("Expecting operand")

                expect_operand = True

                while stack:
                    last_stack_token = stack[-1]

                    if last_stack_token.type in LEXEME_PREFIX_OPERANDS or \
                            LEXEME_INFIX_OPERANDS.index(last_stack_token.type) >= \
                            LEXEME_INFIX_OPERANDS.index(token.type):
                        output.append(stack.pop())
                    else:
                        break

                stack.append(token)

        for op in stack:
            if op.type in LEXEME_OPERANDS:
                output.append(op)
            else:
                raise LexerException("Invalid brackets count")

        return output

    def _get_fact_tokens(self, rule):
        left_side_facts = []

        for token in rule:
            if token.type == LexemeTypes.FACT:
                left_side_facts.append(token)

        return left_side_facts

    def _parse_right_side(self, right_side, parsed_left_side, rule_node):
        if len(right_side) == 1:
            if right_side[0].type == LexemeTypes.FACT:
                lhs_fact_tokens = self._get_fact_tokens(parsed_left_side)

                for token in lhs_fact_tokens:
                    self._graph.add_edge(FactNode(right_side[0].value),
                                         FactNode(token.value), rule=rule_node)

        elif len(right_side) == 2:
            op, val = right_side

            if op.type == LexemeTypes.OP_NOT:
                lhs_fact_tokens = self._get_fact_tokens(parsed_left_side)

                # for token in lhs_fact_tokens:
                #     self._graph.add_edge(FactNode(val.value),
                #                          FactNode(token.value), rule=rule_node)

    def _parse_rule(self, rule):

        left_side, conclusion_op, right_side = self._partition_rule(rule)

        rpl_left_side = self._convert_to_rpl(left_side)

        rule_node = RuleNode(left_side, conclusion_op, right_side)

        self._parse_right_side(right_side, rpl_left_side, rule_node)

        # for i in rpl_left_side:
        #     print(i.value, end=" ")
        #
        # print("")
