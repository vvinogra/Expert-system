import logging
import networkx as nx
import matplotlib.pyplot as plt

from lexeme import *
from .inference_engine_exception import InferenceEngineException


class InferenceEngine:
    def __init__(self, graphic, interactive, verbose, queries, initial_facts, rules):
        self.graphic = graphic
        self.interactive = interactive
        self.verbose = verbose

        self._graph = nx.MultiDiGraph()
        self._queries = queries
        self._initial_facts = initial_facts
        self._rules = rules

        self._initialize_nodes()
        self._apply_initial_facts()
        self._link_rules()

    def _initialize_nodes(self):
        for fact_val in LexemeTypes.FACT:
            self._graph.add_node(Fact(fact_val), value=False)

    def _apply_initial_facts(self):
        for fact in self._initial_facts:
            self._graph.nodes[fact]["value"] = True

    def _link_rules(self):
        for rule in self._rules:
            for r_fact in rule.get_right_side_facts():
                self._graph.add_edge(r_fact, rule)

            for l_fact in rule.get_left_side_facts():
                self._graph.add_edge(rule, l_fact)

    def _show_graph_plot(self):
        nx.draw(self._graph,
                with_labels=True,
                arrows=True,
                pos=nx.circular_layout(self._graph),
                node_color=self._colorized_nodes())

        plt.show(block=True)

    def _colorized_nodes(self):
        ret = []

        for node in self._graph.nodes():
            if type(node) is Fact:
                if node in self._queries:
                    if self._graph.nodes[node]["value"]:
                        ret.append("red")
                    else:
                        ret.append("blue")
                else:
                    if self._graph.nodes[node]["value"]:
                        ret.append("yellow")
                    else:
                        ret.append("gray")
            else:
                ret.append("purple")

        return ret

    def _convert_to_rpn(self, token_list):
        output = []
        stack = []
        expect_operand = True

        for token in token_list:
            if type(token) is Fact:
                if not expect_operand:
                    raise InferenceEngineException("Invalid expression")

                expect_operand = False

                output.append(token)
            elif type(token) is Operator:
                if token.is_prefix_operator():
                    if not expect_operand:
                        raise InferenceEngineException("Invalid expression")

                    expect_operand = True

                    stack.append(token)
                elif token.op == LexemeTypes.LEFT_BRACKET:
                    if not expect_operand:
                        raise InferenceEngineException("Invalid expression")

                    expect_operand = True

                    stack.append(token)
                elif token.op == LexemeTypes.RIGHT_BRACKET:
                    if expect_operand:
                        raise InferenceEngineException("Invalid expression")

                    expect_operand = False

                    while stack:
                        last_token = stack.pop()

                        if last_token.op == LexemeTypes.LEFT_BRACKET:
                            break

                        output.append(last_token)

                    if not stack:
                        raise InferenceEngineException("Invalid brackets count in expression")

                elif token.is_infix_operator():
                    if expect_operand:
                        raise InferenceEngineException("Invalid expression")

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
                raise InferenceEngineException("Invalid brackets count in expression")

        return output

    def _resolve_query(self, query):
        result = []

        if query in self._graph.nodes():
            for neighbor in self._graph.neighbors(query):
                rpn_left_side = self._convert_to_rpn(neighbor.left_side)

                res_left = self._solve_rpn(rpn_left_side)
                #
                # res = neighbor.solve_right_side(res_left)
                #
                # result.append(res)

        # if len(result):
        #     if not all(x == result[0] for x in result):
        #         raise BaseException("Contradiction in facts")
        #     self._graph.nodes[query]["value"] = result[0]
        # else:
        #     self._graph.nodes[query]["value"] = False

    def resolve_queries(self):
        for query in self._queries:
            self._resolve_query(query)
