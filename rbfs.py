from puzzle import Puzzle
from sys import maxsize

open_nodes = 0


def RBFS(initial_state, goal_state):
    global open_nodes
    open_nodes = 1
    start_puzzle = Puzzle(initial_state, goal_state, None, None, 0)
    if not start_puzzle.is_solvable():
        return None
    node = RBFS_search(start_puzzle, maxsize)
    node = node[0]
    return node.find_solution(), open_nodes


def RBFS_search(node, f_limit):
    global open_nodes
    successors = []

    if node.goal_test():
        return node, None
    children = node.generate_children()
    if not len(children):
        return None, maxsize
    count = -1
    for child in children:
        open_nodes += 1
        count += 1
        successors.append((child.evaluation_function, count, child))
    while len(successors):
        successors.sort()
        best_node = successors[0][2]
        if best_node.evaluation_function > f_limit:
            open_nodes -= len(children)
            return None, best_node.evaluation_function
        if len(successors) > 1:
            alternative = successors[1][0]
            result, best_node.evaluation_function = RBFS_search(best_node, min(f_limit, alternative))
        else:
            result, best_node.evaluation_function = RBFS_search(best_node, f_limit)
        successors[0] = (best_node.evaluation_function, successors[0][1], best_node)
        if result is not None:
            break

    return result, None







