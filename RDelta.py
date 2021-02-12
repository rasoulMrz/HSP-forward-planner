from Action import Action

def subs(conds):
    res = []
    conds = list(conds)
    for i in range(len(conds)):
        for j in range(i+1, len(conds)):
            res.append(set([conds[i], conds[j]]))
    return res


def find_applicables(goals, assignments, operator, problem):
    if(len(goals) == 0):
        if(len(assignments) != len(operator.params)):
            actions = []
            for p in operator.params:
                if p not in assignments:
                    for o in problem.objects:
                        extras = {}
                        extras[p] = o
                        extras.update(assignments)
                        actions += find_applicables(goals, extras, operator, problem)
                    return actions
        return [Action(operator, assignments)]

    goal = goals[0]
    args = goal[1:]
    params_list = operator.add_effects._preds[goal[0]]

    actions = []
    for params in params_list:
        extras = {}
        for i in range(len(params)):
            if params[i] in assignments:
                if(assignments[params[i]] != args[i]):
                    extras = None
                    break
            else:
                extras[params[i]] = args[i]
        if extras != None:
            extras.update(assignments)
            actions += find_applicables(goals[1:], extras, operator, problem)

    return actions


def find_actions(goals, problem):
    actions = []
    goals = [g.split() for g in goals]
    for operator in problem.domain.operators:
        assignments = {}
        for g in goals:
            name, params = g[0], g[1:]
            if name not in operator.add_effects._preds:
                assignments = None
                break
            
        if(assignments is not None):
            actions += find_applicables(goals, assignments, operator, problem)
    return actions

def delta2(g, mem, problem):
    if not isinstance(g, set):
        g = g.flat_set()

    if(len(g) == 0):
        return 0
    if(len(g) == 1):
        g1 = list(g)[0]
        if g1 in mem:
            return mem[g1]
        mem[g1] = 1e10
        res = 1e10
        actions = find_actions(g, problem)
        for act in actions:
            res = min(res, 1+delta2(act.preconditions, mem, problem))
        mem[g1] = res
        return res

    if(len(g) == 2):
        lg = list(g)
        res = 1e10
        lg.sort()
        pair = ','.join(lg)
        if pair in mem:
            return mem[pair]
        mem[pair] = 1e20

        actions = find_actions(g, problem)
        for act in actions:
            res = min(res, 1+delta2(act.preconditions, mem, problem))
        
        actions = find_actions(set([lg[0]]), problem)
        for act in actions:
            pre = act.preconditions.flat_set().copy()
            pre.add(lg[1])
            res = min(res, 1+delta2(pre, mem, problem))
        
        actions = find_actions(set([lg[1]]), problem)
        for act in actions:
            pre = act.preconditions.flat_set().copy()
            pre.add(lg[0])
            res = min(res, 1+delta2(pre, mem, problem))
        mem[pair] = res
        return res

    pairs = subs(g)
    res = 0
    for p in pairs:
        d = delta2(p, mem, problem)
        if(d < 1e20):
            res = max(res, d)

    return res