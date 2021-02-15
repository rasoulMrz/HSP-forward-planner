from Utils import read_lines
from Problem import Problem
from Domain import Domain
from Delta import compute_delta, delta2

domain = Domain.from_lines(read_lines("world/domain.txt"))
problem = Problem.from_lines(read_lines("world/sussman-anomaly.txt"), domain)

def check_loop(state, seen):
  for s in seen:
    if(s.contains(state)):
      return True
  return False

def search(state, goal, trajectory, seen):
  new_seen = seen + [state]
  
  if(state.contains(goal)):
        return True, trajectory

  applicables = state.get_applicable_actions(problem)
  
  action_delta_s = []
  for a in applicables:
    a_s = a.apply(state)
    mem = compute_delta(a_s, problem)
    delta = delta2(problem.goals, mem)
    action_delta_s.append((a, delta, a_s))
  
  action_delta_s = sorted(action_delta_s, key=lambda p: p[1])

  for i, tpl in enumerate(action_delta_s):
    a, next_state = tpl[0], tpl[2]
    # next_state = applicables[i].apply(state)
    if(check_loop(next_state, new_seen)):
      continue
    new_trajectory = trajectory + [a]

    result, result_trajectory = search(next_state, goal, new_trajectory, new_seen)
    if result == True:
      return True, result_trajectory 
  return False, []

r, t = search(problem.initial_state, problem.goals, [], [])
for i, a in enumerate(t):
    print(f"{i}:{a}")