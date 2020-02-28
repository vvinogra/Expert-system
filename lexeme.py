import string
from enum import Enum


class RuleNode:
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

    # def _solve_rule(self, graph):

    def _get_fact_tokens(self):
        left_side_facts = []

        for token in self.left_side:
            if token.type == LexemeTypes.FACT:
                left_side_facts.append(token)

        return left_side_facts


class LexemeTypes(Enum):
    FACT = tuple(string.ascii_uppercase)
    LEFT_BRACKET = "("
    RIGHT_BRACKET = ")"
    OP_NOT = "!"
    OP_AND = "+"
    OP_OR = "|"
    OP_XOR = "^"
    OP_IMPLIES = "=>"
    OP_BICONDITION = "<=>"


class Lexeme:
    _infix_operators_list = [
        LexemeTypes.OP_XOR.value,
        LexemeTypes.OP_OR.value,
        LexemeTypes.OP_AND.value,
    ]

    _prefix_operators_list = [
        LexemeTypes.OP_NOT.value,
    ]

    _conclusion_operators_list = [
        LexemeTypes.OP_IMPLIES.value,
        LexemeTypes.OP_BICONDITION.value
    ]

    _other_operators_list = [
        LexemeTypes.LEFT_BRACKET.value,
        LexemeTypes.RIGHT_BRACKET.value,
    ]

    def __init__(self):
        pass

    @staticmethod
    def operators_list():
        return [
            *Lexeme._infix_operators_list,
            *Lexeme._prefix_operators_list,
            *Lexeme._conclusion_operators_list,
            *Lexeme._other_operators_list
        ]

    @staticmethod
    def is_fact(value):
        return value in LexemeTypes.FACT.value


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
        LexemeTypes.OP_XOR.value,
        LexemeTypes.OP_OR.value,
        LexemeTypes.OP_AND.value,
    ]

    prefix_operators_list = [
        LexemeTypes.OP_NOT.value,
    ]

    conclusion_operators_list = [
        LexemeTypes.OP_IMPLIES.value,
        LexemeTypes.OP_BICONDITION.value
    ]

    other_operators_list = [
        LexemeTypes.LEFT_BRACKET.value,
        LexemeTypes.RIGHT_BRACKET.value,
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
        if self.op == LexemeTypes.OP_XOR.value:
            return left ^ right
        elif self.op == LexemeTypes.OP_OR.value:
            return left | right
        elif self.op == LexemeTypes.OP_AND.value:
            return left & right
        elif self.op == LexemeTypes.OP_NOT.value:
            return ~left

    @staticmethod
    def operators_list():
        return [
            *Operator.infix_operators_list,
            *Operator.prefix_operators_list,
            *Operator.conclusion_operators_list,
            *Operator.other_operators_list
        ]


LEXEME_SYMBOLS = [
    LexemeTypes.LEFT_BRACKET,
    LexemeTypes.RIGHT_BRACKET,
    LexemeTypes.OP_NOT,
    LexemeTypes.OP_AND,
    LexemeTypes.OP_OR,
    LexemeTypes.OP_XOR,
    LexemeTypes.OP_IMPLIES,
    LexemeTypes.OP_BICONDITION
]

LEXEME_PREFIX_OPERANDS = [
    LexemeTypes.OP_NOT
]

# Order values in increasing priority
LEXEME_INFIX_OPERANDS = [
    LexemeTypes.OP_XOR,
    LexemeTypes.OP_OR,
    LexemeTypes.OP_AND,
]

LEXEME_OPERANDS = {
    *LEXEME_PREFIX_OPERANDS,
    *LEXEME_INFIX_OPERANDS
}

LEXEME_IMPLICATION_TYPES = [
    LexemeTypes.OP_IMPLIES,
    LexemeTypes.OP_BICONDITION
]
