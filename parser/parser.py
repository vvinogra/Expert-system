from parser.parser_exception import ParserException
from lexeme import *
import networkx as nx


class Parser:

    def __init__(self, filename):
        self._filename = filename

        self._parsed_initial_facts = False
        self._parsed_queries = False
        self.initial_facts = []
        self.queries = []
        self.rules = []

        self._graph = nx.MultiDiGraph()

        # self._initialize_nodes()

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
                    self._parse_rule(line)

                # pass

        # self._resolve_queries()

        # for i in self._graph.nodes:
        #     if type(i) is Fact:
        #         print("i = {}; i1 = {}".format(self._graph.nodes[i], i))

        # print(self._graph[Fact("A")])

        # nx.draw(self._graph,
        #         with_labels=True,
        #         arrows=True,
        #         pos=nx.circular_layout(self._graph),
        #         node_color=self._colorized_nodes())

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
        # plt.show()
        # print(self._queries)
        # print(self._initial_facts)

    # def _initialize_nodes(self):
    #     for fact_val in LexemeTypes.FACT:
    #         self._graph.add_node(Fact(fact_val), value=False)
    # def _colorized_nodes(self):
    #     ret = []
    #
    #     for node in self._graph.nodes():
    #         if type(node) is Fact:
    #             if node in self._queries:
    #                 if self._graph.nodes[node]["value"]:
    #                     ret.append("red")
    #                 else:
    #                     ret.append("blue")
    #             else:
    #                 if self._graph.nodes[node]["value"]:
    #                     ret.append("yellow")
    #                 else:
    #                     ret.append("gray")
    #         else:
    #             ret.append("purple")
    #
    #     return ret

    def _check_for_initial_facts(self, facts):
        if self._parsed_initial_facts:
            raise ParserException("Initial facts line occurred twice")

        for fact in facts[1:]:
            if fact in LexemeTypes.FACT:
                # self._graph.nodes[Fact(fact)]["value"] = True
                self.initial_facts.append(Fact(fact))
                # self._safely_add_node(Fact(fact), value=True)
                # self._initial_facts.append(Lexeme(LexemeTypes.FACT, fact))
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
                # self._queries.append(Fact(query))
                # self._safely_add_node(Fact(query))
                self.queries.append(Fact(query))
            else:
                raise ParserException("Invalid fact in queries")

        self._parsed_queries = True

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

                for op in Operator.operators_list():
                    if cut_line.startswith(op):
                        token_list.append(Operator(op))
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
            if type(token) is Operator and token.is_conclusion_operator():
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

    def _convert_to_rpn(self, token_list):
        output = []
        stack = []
        expect_operand = True

        for token in token_list:
            if type(token) is Fact:
                if not expect_operand:
                    raise ParserException("Expecting operator")

                expect_operand = False

                output.append(token)
            elif type(token) is Operator:
                if token.is_prefix_operator():
                    if not expect_operand:
                        raise ParserException("Expecting operand")

                    expect_operand = True

                    stack.append(token)
                elif token.op == LexemeTypes.LEFT_BRACKET:
                    if not expect_operand:
                        raise ParserException("Expecting operand")

                    expect_operand = True

                    stack.append(token)
                elif token.op == LexemeTypes.RIGHT_BRACKET:
                    if expect_operand:
                        raise ParserException("Expecting operand")

                    expect_operand = False

                    while stack:
                        last_token = stack.pop()

                        if last_token.op == LexemeTypes.LEFT_BRACKET:
                            break

                        output.append(last_token)

                    if not stack:
                        raise ParserException("Invalid brackets count")

                elif token.is_infix_operator():
                    if expect_operand:
                        raise ParserException("Expecting operand")

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
                raise ParserException("Invalid brackets count")

        return output

    def _solve_rpn(self, token_list):
        stack = []

        for token in token_list:
            if type(token) is Fact:
                stack.append(token)
            elif type(token) is Operator:
                if token.is_infix_operator():
                    op1 = stack.pop()
                    op2 = stack.pop()

                    if type(op1) is bool:
                        op1_val = op1
                    else:
                        op1_val = self._graph.nodes[op1]["value"]
                        if not op1_val:
                            self._resolve_query(op1)

                    if type(op2) is bool:
                        op2_val = op2
                    else:
                        op2_val = self._graph.nodes[op2]["value"]
                        if not op2_val:
                            self._resolve_query(op2)

                    stack.append(token.eval(op1_val, op2_val))
                elif token.is_prefix_operator():
                    op = stack.pop()

                    if type(op) is bool:
                        op_val = op
                    else:
                        op_val = self._graph.nodes[op]["value"]
                        if not op_val:
                            self._resolve_query(op)

                    stack.append(token.eval(op_val))

        return stack[0]

    # def _get_fact_tokens(self, rule):
    #     left_side_facts = []
    #
    #     for token in rule:
    #         if type(token) is Fact:
    #             left_side_facts.append(token)
    #
    #     return left_side_facts

    # def _resolve_query(self, query):
    #     result = []
    #
    #     if query in self._graph.nodes():
    #         for neighbor in self._graph.neighbors(query):
    #             rpn_left_side = self._convert_to_rpn(neighbor.left_side)
    #
    #             res_left = self._solve_rpn(rpn_left_side)
    #
    #             res = neighbor.solve_right_side(res_left)
    #
    #             result.append(res)
    #
    #     if len(result):
    #         if not all(x == result[0] for x in result):
    #             raise BaseException("Contradiction in facts")
    #         self._graph.nodes[query]["value"] = result[0]
    #     else:
    #         self._graph.nodes[query]["value"] = False
    #
    # def _resolve_queries(self):
    #     for query in self._queries:
    #         self._resolve_query(query)

    def _link_rule_node(self, rule_node):
        for fact in rule_node.get_right_side_facts():
            self._graph.add_edge(fact, rule_node)

        for fact in rule_node.get_left_side_facts():
            self._graph.add_edge(rule_node, fact)
        # if len(rule_node.right_side) == 1:
        #     val = rule_node.right_side[0]
        #
        #     if type(val) is Fact:
        #         self._graph.add_edge(val, rule_node)
        #
        #         for token in rule_node.get_left_side_facts():
        #             self._graph.add_edge(rule_node,
        #                                  token)
        #     else:
        #         raise ParserException("Invalid right rule side")
        # elif len(rule_node.right_side) == 2:
        #     operator, val = rule_node.right_side
        #
        #     if type(operator) is Operator and operator.is_prefix_operator() \
        #             and type(val) is Fact:
        #         self._graph.add_edge(val, rule_node)
        #
        #         for token in rule_node.get_left_side_facts():
        #             self._graph.add_edge(rule_node,
        #                                  token)
        #     else:
        #         raise ParserException("Invalid right rule side")
        # elif len(rule_node.right_side) == 3:
        #     v1, operator, v2 = rule_node.right_side
        #
        #     if type(operator) is Operator and operator.is_infix_operator() \
        #             and type(v1) is Fact and type(v2) is Fact:
        #
        #         self._graph.add_edge(v1, rule_node)
        #         self._graph.add_edge(v2, rule_node)
        #
        #         for token in rule_node.get_left_side_facts():
        #             self._graph.add_edge(rule_node,
        #                                  token)
        #     else:
        #         raise ParserException("Invalid right rule side")
        # else:
        #     raise ParserException("Invalid right rule side")

    def _parse_rule(self, rule):
        tokenized_rule = self._tokenize_rule(rule)

        left_side, conclusion_op, right_side = self._partition_rule(tokenized_rule)

        rule_node = RuleNode(left_side, conclusion_op, right_side)

        self.rules.append(rule_node)

        # self._link_rule_node(rule_node)

        # self._parse_right_side(right_side, rpn_left_side, rule_node)

        # for i in solved_rpn:
        #     print(i, end=" ")
        #
        # print("")
