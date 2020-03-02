from .lexeme_types import LexemeTypes


class Operator:
    def __init__(self, op):
        self.op = op

    def __str__(self):
        return self.op

    def __repr__(self):
        return self.op


class InfixOperator(Operator):
    # Order values in increasing priority
    infix_operators_list = [
        LexemeTypes.OP_XOR,
        LexemeTypes.OP_OR,
        LexemeTypes.OP_AND,
    ]

    def __init__(self, op):
        if op not in InfixOperator.infix_operators_list:
            raise ValueError("Invalid infix operator")
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
            raise ValueError("Invalid prefix operator")
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
            raise ValueError("Invalid conclusion operator")
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
            raise ValueError("Invalid bracket operator")
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
