from queue import PriorityQueue
from puzzle import Puzzle


def Astar_search(initial_state, goal_state):
    count = 0
    explored = []
    start_node = Puzzle(initial_state, goal_state, None, None, 0, True)
    if not start_node.is_solvable():
        return None
    successors = PriorityQueue()
    successors.put((start_node.evaluation_function, count, start_node))

    while not successors.empty():
        node = successors.get()
        node = node[2]
        explored.append(node.state)
        if node.goal_test():
            return node.find_solution()

        children = node.generate_child()
        for child in children:
            if child.state not in explored:
                count += 1
                successors.put((child.evaluation_function, count, child))
    return None
