import string
from enum import Enum


class Rule:
    def __init__(self, left_side, conclusion_op, right_side):
        self.left_side = left_side
        self.conclusion_op = conclusion_op
        self.right_side = right_side

        self.full_rule = ' '.join(map(str, self.left_side + [self.conclusion_op] + self.right_side))

    def __str__(self):
        return self.full_rule

    def __repr__(self):
        return self.full_rule

    def __hash__(self):
        return hash(self.full_rule)

    def __eq__(self, other):
        return self.full_rule == other.full_rule

    def get_left_side_facts(self):
        left_side_facts = []

        for token in self.left_side:
            if type(token) is Fact:
                left_side_facts.append(token)

        return left_side_facts

    def get_right_side_facts(self):
        right_side_facts = []

        for token in self.right_side:
            if type(token) is Fact:
                right_side_facts.append(token)

        return right_side_facts

    # def solve_right_side(self, res):
        # if len(self.right_side) == 1:
        #     val = self.right_side[0]
        #
        #     if type(val) is Fact:
        #         return res
        #     else:
        #         raise BaseException("Invalid right rule side")
        # elif len(self.right_side) == 2:
        #     operator, val = self.right_side
        #
        #     if type(operator) is PrefixOperator and type(val) is Fact:
        #         return operator.eval(res)
        #     else:
        #         raise BaseException("Invalid right rule side")
        # elif len(self.right_side) == 3:
        #     v1, operator, v2 = self.right_side
        #
        #     if type(operator) is InfixOperator and type(v1) is Fact and type(v2) is Fact:
        #
        #         if operator.op == LexemeTypes.OP_AND:
        #             return res
        #         else:
        #             raise BaseException("Invalid right rule side")
        #     else:
        #         raise BaseException("Invalid right rule side")
        # else:
        #     raise BaseException("Invalid right rule side")

    # def _convert_to_rpn(self, token_list):
    #     output = []
    #     stack = []
    #     expect_operand = True
    #
    #     for token in token_list:
    #         if type(token) is Fact:
    #             if not expect_operand:
    #                 raise InferenceEngineException("Invalid expression")
    #
    #             expect_operand = False
    #
    #             output.append(token)
    #         elif type(token) is Operator:
    #             if token.is_prefix_operator():
    #                 if not expect_operand:
    #                     raise InferenceEngineException("Invalid expression")
    #
    #                 expect_operand = True
    #
    #                 stack.append(token)
    #             elif token.op == LexemeTypes.LEFT_BRACKET:
    #                 if not expect_operand:
    #                     raise InferenceEngineException("Invalid expression")
    #
    #                 expect_operand = True
    #
    #                 stack.append(token)
    #             elif token.op == LexemeTypes.RIGHT_BRACKET:
    #                 if expect_operand:
    #                     raise InferenceEngineException("Invalid expression")
    #
    #                 expect_operand = False
    #
    #                 while stack:
    #                     last_token = stack.pop()
    #
    #                     if last_token.op == LexemeTypes.LEFT_BRACKET:
    #                         break
    #
    #                     output.append(last_token)
    #
    #                 if not stack:
    #                     raise InferenceEngineException("Invalid brackets count in expression")
    #
    #             elif token.is_infix_operator():
    #                 if expect_operand:
    #                     raise InferenceEngineException("Invalid expression")
    #
    #                 expect_operand = True
    #
    #                 while stack:
    #                     last_stack_token = stack[-1]
    #
    #                     # Fix error with brackets
    #                     if last_stack_token.is_prefix_operator() or \
    #                             Operator.infix_operators_list.index(last_stack_token.op) >= \
    #                             Operator.infix_operators_list.index(token.op):
    #                         output.append(stack.pop())
    #                     else:
    #                         break
    #
    #                 stack.append(token)
    #
    #     for op in stack:
    #         if op.is_prefix_operator() or \
    #                 op.is_infix_operator():
    #             output.append(op)
    #         else:
    #             raise InferenceEngineException("Invalid brackets count in expression")
    #
    #     return output


class LexemeTypes:
    FACT = tuple(string.ascii_uppercase)
    LEFT_BRACKET = "("
    RIGHT_BRACKET = ")"
    OP_NOT = "!"
    OP_AND = "+"
    OP_OR = "|"
    OP_XOR = "^"
    OP_IMPLIES = "=>"
    OP_BICONDITION = "<=>"


# class Lexeme:
#     _infix_operators_list = [
#         LexemeTypes.OP_XOR,
#         LexemeTypes.OP_OR,
#         LexemeTypes.OP_AND,
#     ]
#
#     _prefix_operators_list = [
#         LexemeTypes.OP_NOT,
#     ]
#
#     _conclusion_operators_list = [
#         LexemeTypes.OP_IMPLIES,
#         LexemeTypes.OP_BICONDITION
#     ]
#
#     _other_operators_list = [
#         LexemeTypes.LEFT_BRACKET,
#         LexemeTypes.RIGHT_BRACKET,
#     ]
#
#     # def __init__(self):
#     #     pass
#
#     @staticmethod
#     def operators_list():
#         return [
#             *Lexeme._infix_operators_list,
#             *Lexeme._prefix_operators_list,
#             *Lexeme._conclusion_operators_list,
#             *Lexeme._other_operators_list
#         ]
#
#     @staticmethod
#     def is_fact(value):
#         return value in LexemeTypes.FACT


class Fact:
    def __init__(self, name):
        self.name = name
        # self.value = value

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    # def __invert__(self):
    #     return ~self.value
    #
    # def __and__(self, other):
    #     if type(other) is bool:
    #         return self.value & other
    #     elif type(other) is Fact:
    #         return self.value & other.value
    #
    # def __or__(self, other):
    #     if type(other) is bool:
    #         return self.value | other
    #     elif type(other) is Fact:
    #         return self.value | other.value
    #
    # def __xor__(self, other):
    #     if type(other) is bool:
    #         return self.value ^ other
    #     elif type(other) is Fact:
    #         return self.value ^ other.value


# class Lexeme:
#     def __init__(self, l_type, l_value):
#         self.type = l_type
#         self.value = l_value
#
#     def __str__(self):
#         return self.value
#
#     def __repr__(self):
#         return self.value

class Operator:
    # Order values in increasing priority
    # infix_operators_list = [
    #     LexemeTypes.OP_XOR,
    #     LexemeTypes.OP_OR,
    #     LexemeTypes.OP_AND,
    # ]
    #
    # prefix_operators_list = [
    #     LexemeTypes.OP_NOT,
    # ]
    #
    # conclusion_operators_list = [
    #     LexemeTypes.OP_IMPLIES,
    #     LexemeTypes.OP_BICONDITION
    # ]
    #
    # other_operators_list = [
    #     LexemeTypes.LEFT_BRACKET,
    #     LexemeTypes.RIGHT_BRACKET,
    # ]

    def __init__(self, op):
        self.op = op

    def __str__(self):
        return self.op

    def __repr__(self):
        return self.op

    # def is_infix_operator(self):
    #     return self.op in Operator.infix_operators_list
    #
    # def is_prefix_operator(self):
    #     return self.op in Operator.prefix_operators_list
    #
    # def is_conclusion_operator(self):
    #     return self.op in Operator.conclusion_operators_list
    #
    # def eval(self, left, right=None):
    #     if self.op == LexemeTypes.OP_XOR:
    #         return left ^ right
    #     elif self.op == LexemeTypes.OP_OR:
    #         return left | right
    #     elif self.op == LexemeTypes.OP_AND:
    #         return left & right
    #     elif self.op == LexemeTypes.OP_NOT:
    #         return not left
    #
    # @staticmethod
    # def operators_list():
    #     return [
    #         *Operator.infix_operators_list,
    #         *Operator.prefix_operators_list,
    #         *Operator.conclusion_operators_list,
    #         *Operator.other_operators_list
    #     ]


class InfixOperator(Operator):
    # Order values in increasing priority
    infix_operators_list = [
        LexemeTypes.OP_XOR,
        LexemeTypes.OP_OR,
        LexemeTypes.OP_AND,
    ]

    def __init__(self, op):
        if op not in InfixOperator.infix_operators_list:
            raise BaseException("Invalid infix operator")
        super().__init__(op)

    def __str__(self):
        return super().__repr__()

    def __repr__(self):
        return super().__repr__()

    def eval(self, val1, val2):
        if self.op == LexemeTypes.OP_XOR:
            return val1 ^ val2
        elif self.op == LexemeTypes.OP_OR:
            return val1 | val2
        elif self.op == LexemeTypes.OP_AND:
            return val1 & val2


class PrefixOperator(Operator):
    # Order values in increasing priority
    prefix_operators_list = [
        LexemeTypes.OP_NOT
    ]

    def __init__(self, op):
        if op not in PrefixOperator.prefix_operators_list:
            raise BaseException("Invalid prefix operator")
        super().__init__(op)

    def __str__(self):
        return super().__repr__()

    def __repr__(self):
        return super().__repr__()

    def eval(self, val):
        if self.op == LexemeTypes.OP_NOT:
            return not val


class ConclusionOperator(Operator):
    conclusion_operators_list = [
        LexemeTypes.OP_IMPLIES,
        LexemeTypes.OP_BICONDITION
    ]

    def __init__(self, op):
        if op not in ConclusionOperator.conclusion_operators_list:
            raise BaseException("Invalid conclusion operator")
        super().__init__(op)

    def __str__(self):
        return super().__repr__()

    def __repr__(self):
        return super().__repr__()


class BracketOperator(Operator):
    bracket_operators_list = [
        LexemeTypes.LEFT_BRACKET,
        LexemeTypes.RIGHT_BRACKET,
    ]

    def __init__(self, op):
        if op not in BracketOperator.bracket_operators_list:
            raise BaseException("Invalid bracket operator")
        super().__init__(op)

    def __str__(self):
        return super().__repr__()

    def __repr__(self):
        return super().__repr__()


class OperatorFactory:
    operators_list = [
        *BracketOperator.bracket_operators_list,
        *ConclusionOperator.conclusion_operators_list,
        *PrefixOperator.prefix_operators_list,
        *InfixOperator.infix_operators_list
    ]

    @staticmethod
    def get_operator(operator):
        if operator in BracketOperator.bracket_operators_list:
            return BracketOperator(operator)
        elif operator in ConclusionOperator.conclusion_operators_list:
            return ConclusionOperator(operator)
        elif operator in PrefixOperator.prefix_operators_list:
            return PrefixOperator(operator)
        elif operator in InfixOperator.infix_operators_list:
            return InfixOperator(operator)
        else:
            raise ValueError("Invalid operator - {}".format(operator))

