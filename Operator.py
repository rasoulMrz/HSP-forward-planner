from PredicateList import PredicateList
from Utils import read_lines, read_def

class Operator():
    def __init__(self, name, params, preconditions, add_effects, delete_effects):
        self.name = name
        self.params = params
        self.preconditions = preconditions
        self.add_effects = add_effects
        self.delete_effects = delete_effects

    @staticmethod
    def from_lines(lines, predicate_defs):
        name = lines.pop()
        params = [lines.pop() for i in range(read_def(lines, "parameters"))]

        preconditions = PredicateList.from_lines(lines, predicate_defs, "preconditions")
        add_effects = PredicateList.from_lines(lines, predicate_defs, "add-effects")
        delete_effects = PredicateList.from_lines(lines, predicate_defs, "delete-effects")

        return Operator(name, params, preconditions, add_effects, delete_effects)
