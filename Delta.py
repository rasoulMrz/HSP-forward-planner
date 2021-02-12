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
    g = g.flat_set()
    
    if(len(g) == 0):
        return 0
    if(len(g) == 1):
        return mem.get(list(g)[0], 1e10)

    pairs = subs(g, singles=False)
    res = 0
    for p in pairs:
        res = max(res, mem.get(p, 1e10))
    
    print(g, res)
    return res

def compute_delta(state, domain):
    state = state.clone()
    mem = {}
    for a in subs(state.flat_set()):
        mem[a] = 0

    while(True):
        has_change = False
        applicables = state.get_applicable_actions(domain)
        for a in applicables:
            state.add_all(a.add_effects)
            d2 = delta2(a.preconditions, mem)
            adds = subs(state.flat_set())
            for a in adds:
                old = mem.get(a, 1e10)
                new = 1 + d2
                if(new < old):
                    print(a, new)
                    has_change = True
                    mem[a] = new
        input()                    
        if(not has_change):
            return mem
