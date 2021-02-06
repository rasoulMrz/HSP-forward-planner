from Operator import Operator

class Action():
    def __init__(self, operator, assignments):
        self.operator = operator
        self.params = []
        assert len(assignments) ==  len(operator.params)

        for p in operator.params:
            assert p in assignments
            self.params.append(assignments[p])

        self.preconditions = operator.preconditions.unify(assignments)
        self.add_effects = operator.add_effects.unify(assignments)
        self.delete_effects = operator.delete_effects.unify(assignments)

    def apply(self, state):
        assert state.contains(self.preconditions)
        res = state.subtract(self.delete_effects)
        res.add_all(self.add_effects)
        return res

    def __str__(self):
        return "(" + ' '.join([self.operator.name, *self.params]) + ")"