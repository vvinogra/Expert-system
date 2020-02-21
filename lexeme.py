import string


class FactNode:
    def __init__(self, fact_name, value):
        # self._type = l_type
        self._value = fact_name
        self._value = value


class RuleNode:
    def __init__(self, rule_query, rule_result):
        self._rule_q = rule_query
        self._rule_r = rule_result


class Lexeme:
    def __init__(self, l_type, l_value):
        self._type = l_type
        self._value = l_value


LEXEME_TYPES = {
    "FACT": set(string.ascii_uppercase),
    "LEFT_BRACE": "(",
    "RIGHT_BRACE": ")",
    "OP_NOT": "!",
    "OP_AND": "+",
    "OP_OR": "|",
    "OP_XOR": "^",
    "OP_IMPLIES": "=>",
    "OP_BICONDITION": "<=>"
}

LEXEME_OPERATORS = {
    "OP_AND": LEXEME_TYPES["OP_AND"],
    "OP_OR": LEXEME_TYPES["OP_OR"],
    "OP_XOR": LEXEME_TYPES["OP_XOR"],
    "OP_IMPLIES": LEXEME_TYPES["OP_IMPLIES"],
    "OP_BICONDITION": LEXEME_TYPES["OP_BICONDITION"]
}

