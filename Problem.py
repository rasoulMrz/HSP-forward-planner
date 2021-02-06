from PredicateList import PredicateList
from Operator import Operator
from Utils import read_lines, read_def

class Problem():
    def __init__(self, domain, objects, initial_state, goals):
        self.domain = domain
        self.objects = objects
        self.initial_state = initial_state
        self.goals = goals

    @staticmethod
    def from_lines(lines, domain):
        objects = [lines.pop() for i in range(read_def(lines, "objects"))]
        initial_state = PredicateList.from_lines(lines, domain.predicates, "initial-state")
        goals = PredicateList.from_lines(lines, domain.predicates, "goals")
        return Problem(domain, objects, initial_state, goals)