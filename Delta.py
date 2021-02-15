def subs(conds, singles=True):
    res = []
    conds = list(conds)
    for i in range(len(conds)):
        if(singles):
            res.append(conds[i])
        for j in range(i+1, len(conds)):
            s = [conds[i], conds[j]]
            s.sort()
            res.append(','.join(s))
    return res

def delta2(g, mem):
    if not isinstance(g, set):
        g = g.flat_set()
    
    if(len(g) == 0):
        return 0
    if(len(g) == 1):
        return mem.get(list(g)[0], 1e10)

    pairs = subs(g, singles=False)
    res = 0
    for p in pairs:
        res = max(res, mem.get(p, 1e10))
    return res

def compute_delta(state, problem):
    state = state.clone()
    mem = {}
    for a in subs(state.flat_set()):
        mem[a] = 0

    while(True):
        has_change = False
        applicables = state.get_applicable_actions(problem)
        for action in applicables:
            precs = action.preconditions
            add_effects = action.add_effects
            state.add_all(add_effects)
            d2 = delta2(precs, mem)
            adds = subs(add_effects.flat_set())
            for a in adds:
                old = mem.get(a, 1e10)
                new = 1 + d2
                if(new < old):
                    has_change = True
                    mem[a] = new
            
            adds = add_effects.flat_set()
            diff = state.flat_set().difference(adds)
            for a in adds:
                for b in diff:
                    d2 = delta2(precs.flat_set().union(set([b])), mem)
                    s = [a, b]
                    s.sort()
                    pair = ','.join(s)
                    old = mem.get(pair, 1e10)
                    new = 1 + d2
                    if(new < old):
                        has_change = True
                        mem[pair] = new                
        if(not has_change):
            return mem
