def count_inversions(state):
    inversions = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] > state[j]:
                inversions += 1
    return inversions


class Puzzle:
    heuristic = None
    evaluation_function = None
    needs_heuristic = False
    num_of_instances = 0

    def __init__(self, state, goal, parent, action, path_cost, needs_heuristic=False):
        self.parent = parent
        self.goal_state = goal
        self.state = state
        self.action = action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost
        if needs_heuristic:
            self.needs_heuristic = True
            self.generate_heuristic()
            self.evaluation_function = self.heuristic + self.path_cost
        Puzzle.num_of_instances += 1

    def is_solvable(self):
        start_state = [num for num in self.state if num != " "]
        end_state = [num for num in self.goal_state if num != " "]

        start_inversions = count_inversions(start_state)
        goal_inversions = count_inversions(end_state)

        if start_inversions % 2 == goal_inversions % 2:
            return True
        else:
            return False

    def generate_heuristic(self):
        self.heuristic = 0
        for num in range(1, 9):
            distance = abs(self.state.index(num) - self.goal_state.index(num))
            i = int(distance / 3)
            j = int(distance % 3)
            self.heuristic = self.heuristic + i + j

    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False

    def find_legal_actions(self, i, j):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0:  # up is disable
            legal_action.remove('U')
        elif i == 2:  # down is disable
            legal_action.remove('D')
        if j == 0:
            legal_action.remove('L')
        elif j == 2:
            legal_action.remove('R')

        legal_action = self.critical_optimization(legal_action)
        return legal_action

    def critical_optimization(self, legal_actions):
        if self.action is not None:
            if self.action == 'U':
                legal_actions.remove('D')
            elif self.action == 'D':
                legal_actions.remove('U')
            elif self.action == 'L':
                legal_actions.remove('R')
            elif self.action == 'R':
                legal_actions.remove('L')
        return legal_actions

    def generate_child(self):
        children = []
        x = self.state.index(" ")
        i = int(x / 3)
        j = int(x % 3)
        legal_actions = self.find_legal_actions(i, j)

        for action in legal_actions:
            new_state = self.state.copy()
            if action == 'U':
                new_state[x], new_state[x - 3] = new_state[x - 3], new_state[x]
            elif action == 'D':
                new_state[x], new_state[x + 3] = new_state[x + 3], new_state[x]
            elif action == 'L':
                new_state[x], new_state[x - 1] = new_state[x - 1], new_state[x]
            elif action == 'R':
                new_state[x], new_state[x + 1] = new_state[x + 1], new_state[x]
            children.append(Puzzle(new_state, self.goal_state, self, action, 1, self.needs_heuristic))
        return children

    def find_solution(self):
        solution = [self.state]
        path = self
        while path.parent is not None:
            path = path.parent
            solution.append(path.state)
        solution.reverse()
        return solution
