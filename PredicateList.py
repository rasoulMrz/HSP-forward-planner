from Utils import read_def

class PredicateList():
    def __init__(self):
        self.preds = {}
    
    def add(self, name, params):
        if(name not in self.preds):
            self.preds[name] = [params]
        else:
            self.preds[name].append(params)

    def unify(self, assignments):
        trgt = PredicateList()

        for name in self.preds:
            params_list = self.preds[name]
            for params in params_list:
                trgt.add(name, list(map(lambda p: assignments[p], params)))

        return trgt

    def contains(self, target):
        for name in target.preds:        
            if name not in self.preds:
                return False
            params_list = target.preds[name]
            for params in params_list:
                if params not in self.preds[name]:
                    return False
        
        return True

    def subtract(self, target):
        ans = PredicateList()

        for name in self.preds:
            t = []
            if name in target.preds:
                t = target.preds[name]

            params_list = list(filter(lambda p: p not in t, self.preds[name]))
            if(len(params_list) > 0):
                ans.preds[name] = params_list
        return ans


    def add_all(self, target):
        for name in target.preds:
            t = []
            if name in self.preds:
                t = self.preds[name]
            else:
                self.preds[name] = t

            for p in target.preds[name]:
                if p not in t:
                    t.append(p)

    def get_applicable_actions(self, domain):
        actions = []
        for operator in domain.operators:
            preconditions = operator.preconditions

            flat_precs = []
            for name in preconditions.preds:
                if name not in self.preds:
                    flat_precs = None
                    break
                flat_precs += [(name, params) for params in preconditions.preds[name]]
            
            if flat_precs is not None:
                actions += self.find_applicables({}, flat_precs, operator, domain)
        
        return actions
            
            
    def find_applicables(self, assignments, rem_precs, operator, domain):
        if(len(rem_precs) == 0):
            ## FIXME
            # if(len(assignments) != len(operator.params)):
            #     for p in operator.params:
            #         if p not in assignments:
            #             for o in domain.objects:
            #                 assignments[p] = 
            return [Action(operator, assignments)]
        
        prec = rem_precs[0]
        args = prec[1]
        params_list = self.preds[prec[0]]
        
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
                actions += self.find_applicables(extras, rem_precs[1:], operator, domain)

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
    
    def __str__(self):
        lines = []
        for name in self.preds:
            for params in self.preds[name]:
                lines.append(' '.join([name, *params]))
        
        return '\n'.join(lines)


from Action import Action
