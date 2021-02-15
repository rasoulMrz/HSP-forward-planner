from Utils import read_def

class PredicateList():
    def __init__(self):
        self._preds = {}
        self._flat_set = set()

    def add(self, name, params):
        if(name not in self._preds):
            self._preds[name] = [params]
        else:
            self._preds[name].append(params)
        self._flat_set.add(' '.join([name, *params]))

    def unify(self, assignments):
        trgt = PredicateList()

        for name in self._preds:
            params_list = self._preds[name]
            for params in params_list:
                trgt.add(name, list(map(lambda p: assignments[p], params)))

        return trgt

    def flat_set(self):
        return self._flat_set

    def contains(self, other):
        return other.flat_set().issubset(self.flat_set())

    def subtract(self, target):
        ans = PredicateList()

        for name in self._preds:
            t = []
            if name in target._preds:
                t = target._preds[name]

            params_list = filter(lambda p: p not in t, self._preds[name])
            for p in params_list:
                ans.add(name, p)
        return ans


    def add_all(self, target):
        diff = target._flat_set.difference(self._flat_set)
        for a in diff:
            p = a.split()
            self.add(p[0], p[1:])
            
    def get_applicable_actions(self, problem):
        actions = []
        for operator in problem.domain.operators:
            preconditions = operator.preconditions

            flat_precs = []
            for name in preconditions._preds:
                if name not in self._preds:
                    flat_precs = None
                    break
                flat_precs += [(name, params) for params in preconditions._preds[name]]
            
            if flat_precs is not None:
                actions += self.find_applicables({}, flat_precs, operator, problem)
        
        return actions


    def find_applicables(self, assignments, rem_precs, operator, problem):
        if(len(rem_precs) == 0):
            if(len(assignments) != len(operator.params)):
                actions = []
                for p in operator.params:
                    if p not in assignments:
                        for o in problem.objects:
                            extras = {}
                            extras[p] = o
                            extras.update(assignments)
                            actions += find_applicables(extras, rem_precs, operator, problem)
                        return actions
            return [Action(operator, assignments)]
        
        prec = rem_precs[0]
        args = prec[1]
        params_list = self._preds[prec[0]]
        
        actions = []
        for params in params_list:
            extras = {}
            for i in range(len(params)):
                if args[i] in assignments:
                    if(assignments[args[i]] != params[i]):
                        extras = None
                        break
                else:
                    extras[args[i]] = params[i]
            if extras != None:
                extras.update(assignments)
                actions += self.find_applicables(extras, rem_precs[1:], operator, problem)

        return actions


    @staticmethod
    def from_lines(lines, predicate_defs, title):
        pl = PredicateList()
        count = read_def(lines, title)

        for i in range(count):
            name = lines.pop()

            pcount = predicate_defs[name]
            params = [lines.pop() for i in range(pcount)]

            pl.add(name, params)

        return pl

    def clone(self):
        res = PredicateList()
        for name in self._preds:
            res._preds[name] = self._preds[name][:]
        res._flat_set = self._flat_set.copy()
        return res

    def __str__(self):
        return '\n'.join(self.flat_set())


from Action import Action
