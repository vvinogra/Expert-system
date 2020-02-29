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

    def solve_right_side(self, res):
        if len(self.right_side) == 1:
            val = self.right_side[0]

            if type(val) is Fact:
                return res
            else:
                raise BaseException("Invalid right rule side")
        elif len(self.right_side) == 2:
            operator, val = self.right_side

            if type(operator) is Operator and operator.is_prefix_operator() \
                    and type(val) is Fact:
                return operator.eval(res)
            else:
                raise BaseException("Invalid right rule side")
        elif len(self.right_side) == 3:
            v1, operator, v2 = self.right_side

            if type(operator) is Operator and operator.is_infix_operator() \
                    and type(v1) is Fact and type(v2) is Fact:

                if operator.op == LexemeTypes.OP_AND:
                    return res
                else:
                    raise BaseException("Invalid right rule side")
            else:
                raise BaseException("Invalid right rule side")
        else:
            raise BaseException("Invalid right rule side")


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
    infix_operators_list = [
        LexemeTypes.OP_XOR,
        LexemeTypes.OP_OR,
        LexemeTypes.OP_AND,
    ]

    prefix_operators_list = [
        LexemeTypes.OP_NOT,
    ]

    conclusion_operators_list = [
        LexemeTypes.OP_IMPLIES,
        LexemeTypes.OP_BICONDITION
    ]

    other_operators_list = [
        LexemeTypes.LEFT_BRACKET,
        LexemeTypes.RIGHT_BRACKET,
    ]

    def __init__(self, op):
        self.op = op

    def __str__(self):
        return self.op

    def __repr__(self):
        return self.op

    def is_infix_operator(self):
        return self.op in Operator.infix_operators_list

    def is_prefix_operator(self):
        return self.op in Operator.prefix_operators_list

    def is_conclusion_operator(self):
        return self.op in Operator.conclusion_operators_list

    def eval(self, left, right=None):
        if self.op == LexemeTypes.OP_XOR:
            return left ^ right
        elif self.op == LexemeTypes.OP_OR:
            return left | right
        elif self.op == LexemeTypes.OP_AND:
            return left & right
        elif self.op == LexemeTypes.OP_NOT:
            return not left

    @staticmethod
    def operators_list():
        return [
            *Operator.infix_operators_list,
            *Operator.prefix_operators_list,
            *Operator.conclusion_operators_list,
            *Operator.other_operators_list
        ]


# LEXEME_SYMBOLS = [
#     LexemeTypes.LEFT_BRACKET,
#     LexemeTypes.RIGHT_BRACKET,
#     LexemeTypes.OP_NOT,
#     LexemeTypes.OP_AND,
#     LexemeTypes.OP_OR,
#     LexemeTypes.OP_XOR,
#     LexemeTypes.OP_IMPLIES,
#     LexemeTypes.OP_BICONDITION
# ]
#
# LEXEME_PREFIX_OPERANDS = [
#     LexemeTypes.OP_NOT
# ]
#
# # Order values in increasing priority
# LEXEME_INFIX_OPERANDS = [
#     LexemeTypes.OP_XOR,
#     LexemeTypes.OP_OR,
#     LexemeTypes.OP_AND,
# ]
#
# LEXEME_OPERANDS = {
#     *LEXEME_PREFIX_OPERANDS,
#     *LEXEME_INFIX_OPERANDS
# }
#
# LEXEME_IMPLICATION_TYPES = [
#     LexemeTypes.OP_IMPLIES,
#     LexemeTypes.OP_BICONDITION
# ]
