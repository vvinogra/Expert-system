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
            # If we have rule with bicondition conclusion operator then we split it to 2 rules
            if rule.conclusion_op.op == LexemeTypes.OP_BICONDITION:
                self._log_verbose("BICONDITION RULE WAS FOUND")
                new_rule = Rule(rule.left_side,
                                OperatorFactory.get_operator(LexemeTypes.OP_IMPLIES), rule.right_side)

                new_swap_rule = Rule(rule.right_side,
                                     OperatorFactory.get_operator(LexemeTypes.OP_IMPLIES), rule.left_side)

                self._log_verbose("SPLITTING BICONDITION RULE")
                self._log_verbose("FIRST NEW RULE = \"{}\"".format(new_rule))
                self._log_verbose("SECOND NEW RULE = \"{}\"".format(new_swap_rule))

                for r_fact in new_rule.get_right_side_facts():
                    self._graph.add_edge(r_fact, new_rule)

                for l_fact in new_rule.get_left_side_facts():
                    self._graph.add_edge(new_rule, l_fact)

                for r_fact in new_swap_rule.get_right_side_facts():
                    self._graph.add_edge(r_fact, new_swap_rule)

                for l_fact in new_swap_rule.get_left_side_facts():
                    self._graph.add_edge(new_swap_rule, l_fact)
            else:
                for r_fact in rule.get_right_side_facts():
                    self._graph.add_edge(r_fact, rule)

                for l_fact in rule.get_left_side_facts():
                    self._graph.add_edge(rule, l_fact)

    def _log_verbose(self, msg, *args, **kwargs):
        if self.verbose:
            logging.info(msg, *args, **kwargs)

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
            elif type(token) is PrefixOperator:
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

                found_bracket = False

                while stack:
                    last_token = stack.pop()

                    if last_token.op == LexemeTypes.LEFT_BRACKET:
                        found_bracket = True
                        break

                    output.append(last_token)

                if not found_bracket:
                    raise InferenceEngineException("Invalid brackets count in expression")

            elif type(token) is InfixOperator:
                if expect_operand:
                    raise InferenceEngineException("Invalid expression")

                expect_operand = True

                while stack:
                    last_stack_token = stack[-1]

                    if type(last_stack_token) is PrefixOperator or \
                            (type(last_stack_token) is InfixOperator and
                                InfixOperator.infix_operators_list.index(last_stack_token.op) >=
                                InfixOperator.infix_operators_list.index(token.op)):
                        output.append(stack.pop())
                    else:
                        break

                stack.append(token)

        while stack:
            op = stack.pop()

            if type(op) is PrefixOperator or \
                    type(op) is InfixOperator:
                output.append(op)
            else:
                raise InferenceEngineException("Invalid brackets count in expression")

        return output

    def _solve_rpn(self, token_list, dependent_side):
        stack = []

        for token in token_list:
            if type(token) is Fact:
                # hard_or and hard_biconditional tests are not passing
                self._log_verbose("RESOLVING FACT DEPENDENCY: {}".format(token))
                # if token not in self._initial_facts:
                if dependent_side:
                    self._resolve_query(token, dependent_side)

                stack.append(token)
            elif type(token) is InfixOperator:
                op1 = stack.pop()
                op2 = stack.pop()

                if type(op1) is bool:
                    op1_val = op1
                else:
                    op1_val = self._graph.nodes[op1]["value"]

                if type(op2) is bool:
                    op2_val = op2
                else:
                    op2_val = self._graph.nodes[op2]["value"]

                stack.append(token.eval(op1_val, op2_val))
            elif type(token) is PrefixOperator:
                op = stack.pop()

                if type(op) is bool:
                    op_val = op
                else:
                    op_val = self._graph.nodes[op]["value"]

                stack.append(token.eval(op_val))

        if type(stack[0]) is Fact:
            return self._graph.nodes[stack[0]]["value"]
        else:
            return stack[0]

    def _solve_right_side(self, res, right_side):
        if len(right_side) == 1:
            val = right_side[0]

            if type(val) is Fact:
                return res
            else:
                raise InferenceEngineException("Invalid right rule side")
        elif len(right_side) == 2:
            operator, val = right_side

            if type(operator) is PrefixOperator and type(val) is Fact:
                return operator.eval(res)
            else:
                raise InferenceEngineException("Invalid right rule side")
        elif len(right_side) == 3:
            v1, operator, v2 = right_side

            if type(operator) is InfixOperator and type(v1) is Fact and type(v2) is Fact:
                if operator.op == LexemeTypes.OP_AND:
                    return res
                else:
                    return None
            else:
                raise InferenceEngineException("Invalid right rule side")
        else:
            raise InferenceEngineException("Invalid right rule side")

    def _resolve_query(self, query, dependent_side=None):
        result = []

        if query in self._initial_facts:
            result.append(self._graph.nodes[query]["value"])
            self._log_verbose("FACT \"{}\" WAS FOUND IN INITIAL FACTS".format(query))

        self._log_verbose("CHECKING FACT(\"{}\") RULES".format(query))

        for neighbor in self._graph.neighbors(query):
            if dependent_side and neighbor.left_side == dependent_side:
                continue
            self._log_verbose("SOLVING RULE: {}".format(neighbor))

            rpn_left_side = self._convert_to_rpn(neighbor.left_side)
            self._log_verbose("RPN: {}".format(rpn_left_side))

            res_left = self._solve_rpn(rpn_left_side, neighbor.right_side)

            self._log_verbose("RULE EXPRESSION EQUALS: {}".format(res_left))

            res = self._solve_right_side(res_left, neighbor.right_side)

            if res is None:
                self._log_verbose("CAN'T DETERMINE FACT: {}".format(query))
                continue

            result.append(res)

        if len(result):
            if not all(x == result[0] for x in result):
                raise InferenceEngineException("Contradiction in facts")
            self._graph.nodes[query]["value"] = result[0]
        else:
            self._graph.nodes[query]["value"] = False

        self._log_verbose("QUERY \"{q}\" VALUE EQUALS: {v}".format(q=query, v=self._graph.nodes[query]["value"]))

    def print_queries(self):
        for query in self._queries:
            logging.info("{query} = {value}".format(query=query, value=self._graph.nodes[query]["value"]))

    def resolve_queries(self):
        for query in self._queries:
            self._log_verbose("RESOLVING QUERY: {}".format(query))
            self._resolve_query(query)
            # logging.info("{query} = {value}".format(query=query, value=self._graph.nodes[query]["value"]))

        self.print_queries()

        if self.graphic:
            self._show_graph_plot()
