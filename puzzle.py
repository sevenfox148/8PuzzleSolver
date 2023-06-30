def count_inversions(state):
    inversions = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] > state[j]:
                inversions += 1
    return inversions


class Puzzle:

    __heuristic = None
    evaluation_function = None

    def __init__(self, state, goal, parent, action, path_cost):
        self.parent = parent
        self.__goal_state = goal
        self.state = state
        self.__action = action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost

        self.__generate_heuristic()
        self.evaluation_function = self.__heuristic + self.path_cost

    def is_solvable(self):
        start_state = [num for num in self.state if num != " "]
        end_state = [num for num in self.__goal_state if num != " "]

        start_inversions = count_inversions(start_state)
        goal_inversions = count_inversions(end_state)

        if start_inversions % 2 == goal_inversions % 2:
            return True
        else:
            return False

    def __generate_heuristic(self):
        self.__heuristic = 0
        for num in range(1, 9):
            distance = abs(self.state.index(num) - self.__goal_state.index(num))
            i = int(distance / 3)
            j = int(distance % 3)
            self.__heuristic = self.__heuristic + i + j

    def goal_test(self):
        if self.state == self.__goal_state:
            return True
        return False

    def __find_legal_actions(self, i, j):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0:
            legal_action.remove('U')
        elif i == 2:
            legal_action.remove('D')
        if j == 0:
            legal_action.remove('L')
        elif j == 2:
            legal_action.remove('R')

        legal_action = self.__critical_optimization(legal_action)
        return legal_action

    def __critical_optimization(self, legal_actions):
        if self.__action is not None:
            if self.__action == 'U':
                legal_actions.remove('D')
            elif self.__action == 'D':
                legal_actions.remove('U')
            elif self.__action == 'L':
                legal_actions.remove('R')
            elif self.__action == 'R':
                legal_actions.remove('L')
        return legal_actions

    def generate_children(self):
        children = []
        x = self.state.index(" ")
        i = int(x / 3)
        j = int(x % 3)
        legal_actions = self.__find_legal_actions(i, j)

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
            children.append(Puzzle(new_state, self.__goal_state, self, action, 1))
        return children

    def find_solution(self):
        solution = [self.state]
        path = self
        while path.parent is not None:
            path = path.parent
            solution.append(path.state)
        solution.reverse()
        return solution
