import string


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
