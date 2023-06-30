from queue import PriorityQueue
from puzzle import Puzzle


def Astar(initial_state, goal_state):
    count = 1
    explored = []
    start_node = Puzzle(initial_state, goal_state, None, None, 0)
    if not start_node.is_solvable():
        return None
    successors = PriorityQueue()
    successors.put((start_node.evaluation_function, -count, start_node))

    while not successors.empty():
        node = successors.get()
        node = node[2]
        explored.append(node.state)
        if node.goal_test():
            return node.find_solution(), count

        children = node.generate_children()
        for child in children:
            is_explored = any(child.state == explored_state for explored_state in explored)
            if not is_explored:
                count += 1
                successors.put((child.evaluation_function, -count, child))

    return None
