from Operator import Operator
from PredicateList import PredicateList
from Utils import read_lines, read_def

class Domain():
    def __init__(self, predicates, operators):
        self.predicates = predicates
        self.operators = operators

    @staticmethod
    def from_lines(lines):
        predicates = Domain.read_predicates(lines)
        operators = Domain.read_operators(lines, predicates)
        return Domain(predicates, operators)
        
    @staticmethod
    def read_operators(lines, predicates):
        count = read_def(lines, "operators")
        operators = []
        for i in range(count):
            operators.append(Operator.from_lines(lines, predicates))
        
        return operators
    
    @staticmethod
    def read_predicates(lines):
        count = read_def(lines, "predicates")

        preds = {}
        for i in range(count):
            name, pc = lines.pop().split(":")
            preds[name] = int(pc)
        
        return preds