from .fact import Fact


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
