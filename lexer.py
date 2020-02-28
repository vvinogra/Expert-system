from lexer_exception import LexerException
from lexeme import *
import networkx as nx
import matplotlib.pyplot as plt


class Lexer:

    def __init__(self, filename):
        self._filename = filename

        self._parsed_initial_facts = False
        self._parsed_queries = False
        self._initial_facts = []
        self._queries = []

        self._graph = nx.MultiDiGraph()

        self._initialize_nodes()

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

                    # for i in rule:
                    #     print(i, end=" ")
                    # print("")
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

        self._resolve_queries()

        # for i in self._graph.nodes:
        #     if type(i) is Fact:
        #         print("i = {}; i1 = {}".format(self._graph.nodes[i], i))

        # print(self._graph[Fact("A")])

        nx.draw(self._graph,
                with_labels=True,
                arrows=True,
                pos=nx.circular_layout(self._graph),
                node_color=self._colorized_nodes())

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
        # print(self._initial_facts)

    def _initialize_nodes(self):
        for fact_val in LexemeTypes.FACT.value:
            self._graph.add_node(Fact(fact_val), value=False)

    # def _safely_add_node(self, node, **attr):
    #     if node not in self._graph.nodes:
    #         self._graph.add_node(node, **attr)
    #         return True
    #
    #     return False

    def _colorized_nodes(self):
        ret = []

        for node in self._graph.nodes():
            if type(node) is Fact:
                if self._graph.nodes[node]["value"]:
                    ret.append("red")
                else:
                    ret.append("blue")
            else:
                ret.append("yellow")

        return ret

    def _check_for_initial_facts(self, facts):
        if self._parsed_initial_facts:
            raise LexerException("Initial facts line occurred twice")

        for fact in facts[1:]:
            if fact in LexemeTypes.FACT.value:
                self._graph.nodes[Fact(fact)]["value"] = True
                self._initial_facts.append(Fact(fact))
                # self._safely_add_node(Fact(fact), value=True)
                # self._initial_facts.append(Lexeme(LexemeTypes.FACT, fact))
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
                # self._queries.append(Fact(query))
                # self._safely_add_node(Fact(query))
                self._queries.append(Fact(query))
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
                lexeme_list.append(Fact(line[i]))
            else:
                cut_line = line[i:]
                operand_found = False

                for op in Operator.operators_list():
                    if cut_line.startswith(op):
                        lexeme_list.append(Operator(op))
                        chars_to_skip = len(op) - 1
                        operand_found = True

                if not operand_found:
                    raise LexerException("Invalid operator")

        return lexeme_list

    def _partition_rule(self, rule):
        left_side = []
        right_side = []
        conclusion_op = None

        for token in rule:
            if type(token) is Operator and token.is_conclusion_operator():
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
            if type(token) is Fact:
                if not expect_operand:
                    raise LexerException("Expecting operator")

                expect_operand = False

                output.append(token)
            elif type(token) is Operator:
                if token.is_prefix_operator():
                    if not expect_operand:
                        raise LexerException("Expecting operand")

                    expect_operand = True

                    stack.append(token)
                elif token.op == LexemeTypes.LEFT_BRACKET:
                    if not expect_operand:
                        raise LexerException("Expecting operand")

                    expect_operand = True

                    stack.append(token)
                elif token.op == LexemeTypes.RIGHT_BRACKET:
                    if expect_operand:
                        raise LexerException("Expecting operand")

                    expect_operand = False

                    while stack:
                        last_token = stack.pop()

                        if last_token.op == LexemeTypes.LEFT_BRACKET:
                            break

                        output.append(last_token)

                    if not stack:
                        raise LexerException("Invalid brackets count")

                elif token.is_infix_operator():
                    if expect_operand:
                        raise LexerException("Expecting operand")

                    expect_operand = True

                    while stack:
                        last_stack_token = stack[-1]

                        if last_stack_token.is_prefix_operator() or \
                                Operator.infix_operators_list.index(last_stack_token.op) >= \
                                Operator.infix_operators_list.index(token.op):
                            output.append(stack.pop())
                        else:
                            break

                    stack.append(token)

        for op in stack:
            if op.is_prefix_operator() or \
                    op.is_infix_operator():
                output.append(op)
            else:
                raise LexerException("Invalid brackets count")

        return output

    def _solve_rpl(self, token_list):
        stack = []

        for token in token_list:
            if type(token) is Fact:
                stack.append(token)
            elif type(token) is Operator:
                if token.is_infix_operator():
                    op1 = stack.pop()
                    op2 = stack.pop()

                    # if op1 in self._initial_facts:
                    #     self._graph.nodes[op1]["value"] = True
                    if self._graph.nodes[op1]["value"] is False:
                        self._resolve_query(op1)

                    if self._graph.nodes[op2]["value"] is False:
                        self._resolve_query(op2)

                    # if op2 in self._initial_facts:
                    #     op2.value = True
                    # elif op2.value is None:
                    #     self._resolve_query(op2)

                    stack.append(token.eval(self._graph.nodes[op1]["value"], self._graph.nodes[op2]["value"]))
                elif token.is_prefix_operator():
                    op = stack.pop()

                    stack.append(token.eval(self._graph.nodes[op]["value"]))

        return stack[0]

    def _get_fact_tokens(self, rule):
        left_side_facts = []

        for token in rule:
            if type(token) is Fact:
                left_side_facts.append(token)

        return left_side_facts

    def _resolve_query(self, query):
        result = []

        if query in self._graph.nodes():
            for neighbor in self._graph.neighbors(query):
                rpl_left_side = self._convert_to_rpl(neighbor.left_side)

                res = self._solve_rpl(rpl_left_side)

                result.append(res)

        if len(result):
            self._graph.nodes[query]["value"] = all(x for x in result)
        else:
            self._graph.nodes[query]["value"] = False

    def _resolve_queries(self):
        for query in self._queries:
            self._resolve_query(query)

        # print(self._graph.nodes())
        # for i in self._queries:
        #     print("i = {}".format(i.value))

    def _link_rule_node(self, rule_node):
        if len(rule_node.right_side) == 1:
            val = rule_node.right_side[0]

            if type(val) is Fact:
                self._graph.add_edge(val, rule_node)

                lhs_fact_tokens = self._get_fact_tokens(rule_node.left_side)

                for token in lhs_fact_tokens:
                    self._graph.add_edge(rule_node,
                                         token)
            else:
                raise LexerException("Invalid right rule side")

        pass

    def _parse_right_side(self, right_side, parsed_left_side, rule_node):
        if len(right_side) == 1:
            if type(right_side[0]) is Fact:
                self._graph.add_edge(right_side[0], rule_node)

                lhs_fact_tokens = self._get_fact_tokens(parsed_left_side)

                for token in lhs_fact_tokens:
                    self._graph.add_edge(rule_node,
                                         token)
            else:
                raise LexerException("Invalid right rule side")
        elif len(right_side) == 2:
            op, val = right_side

            if type(op) is Operator and op.op == LexemeTypes.OP_NOT.value \
                    and type(val) is Fact:
                lhs_fact_tokens = self._get_fact_tokens(parsed_left_side)

                self._graph.add_edge(val, rule_node)

                for token in lhs_fact_tokens:
                    self._graph.add_edge(rule_node,
                                         token)
            else:
                raise LexerException("Invalid right rule side")
        elif len(right_side) == 3:
            operand1, operator, operand2 = right_side

            # if operator.type == LexemeTypes.OP_AND:
            #     lhs_fact_tokens = self._get_fact_tokens(parsed_left_side)
            #
            #     # for token in lhs_fact_tokens:
            #     #     self._graph.add_edge(Fact(val.value),
            #     #                          Fact(token.value), rule=rule_node)
            # else:
            #     raise LexerException("Invalid right rule side")

    def _parse_rule(self, rule):

        left_side, conclusion_op, right_side = self._partition_rule(rule)

        rpl_left_side = self._convert_to_rpl(left_side)

        rule_node = RuleNode(left_side, conclusion_op, right_side)

        self._parse_right_side(right_side, rpl_left_side, rule_node)

        # for i in solved_rpl:
        #     print(i, end=" ")
        #
        # print("")
