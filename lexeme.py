import string


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
    "OP_BICONDITION": "<=>",
}
