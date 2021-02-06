from Utils import read_lines
from Problem import Problem
from Domain import Domain

domain = Domain.from_lines(read_lines("world/domain.txt"))

problem = Problem.from_lines(read_lines("world/sussman-anomaly.txt"), domain)

state = problem.initial_state
seen = []

while(True):
    seen.append(state)
    print("Goals:")
    print(problem.goals)
    print("State: ")
    print(state)
    if(state.contains(problem.goals)):
        print("GOAL ACHIEVED!")
        break
    print("applicables: ")
    
    applicables = state.get_applicable_actions(domain)
    for i, a in enumerate(applicables):
        print(i, a)
    
    next_state = None
    while(next_state is None):
        i = int(input("Select action:"))
        next_state = applicables[i].apply(state)
        for s in seen:
            if(s.contains(next_state)):
                print("Loop detected! Choose something else!")
                next_state = None
                break
    state = next_state
