import string
from enum import Enum


class FactNode:
    def __init__(self, fact_name, value):
        self._value = fact_name
        self._value = value


class RuleNode:
    def __init__(self, rule_query, rule_result):
        self._rule_q = rule_query
        self._rule_r = rule_result


class Lexeme:
    def __init__(self, l_type, l_value):
        self.type = l_type
        self.value = l_value


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
