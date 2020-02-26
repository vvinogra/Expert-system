import string
from enum import Enum


class RuleNode:
    def __init__(self, left_side, conclusion_op, right_side):
        self._left_side = left_side
        self._conclusion_op = conclusion_op
        self._right_side = right_side

        self.full_rule = ' '.join(map(str, self._left_side + [self._conclusion_op] + self._right_side))

    def __str__(self):
        return self.full_rule

    def __repr__(self):
        return self.full_rule

    def __hash__(self):
        return hash(self.full_rule)

    def __eq__(self, other):
        return self.full_rule == other.full_rule


class FactNode:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Lexeme:
    def __init__(self, l_type, l_value):
        self.type = l_type
        self.value = l_value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


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
