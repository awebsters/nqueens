
import random


# Implement a solver that returns a list of queen's locations
#  - Make sure the list is the right length, and uses the numbers from 0 .. BOARD_SIZE-1

def print_answer(solve):
    for row in range(len(solve)):
        for col in range(len(solve)):
            print('Q' if solve[col] == row else '_', end=" ")
        print("")


def initialize(board_size):
    csp = {'vertices': [], 'edges': []}

    csp['vertices'].append(random.randint(0, board_size - 1))
    csp['edges'].append(set())

    for col in range(1, board_size):

        conflicts = generate_row_conflicts(col, csp, board_size)

        min_rows = degree_compare(conflicts)
        min_row = random.choice(min_rows)
        min_edges = conflicts[min_row]
        csp['vertices'].append(min_row)
        csp['edges'].append(min_edges)

        for edge in min_edges:
            csp['edges'][edge].add(col)

    '''
    vertices = list(range(0, board_size+1))
    random.shuffle(vertices)
    csp['vertices'] = vertices

    for vertex in range(len(vertices)):
        vertex_1 = (csp['vertices'][vertex], vertex)

        edges = set()

        for check_vertex in range(len(vertices)):
            vertex_2 = (csp['vertices'][check_vertex], check_vertex)

            if vertex == check_vertex:
                continue
            elif does_conflict(vertex_1, vertex_2):
                edges.add(check_vertex)

        csp['edges'].append(edges)
    '''
    return csp


def solve(board_size):

    # This almost certainly is a wrong answer!
    answer = initialize(board_size)
    while True:
        result = min_conflicts(answer, board_size)
        if result:
            break
        answer = initialize(board_size)

    return answer['vertices']


def min_conflicts(csp, max_steps):
    board_size = len(csp['vertices'])

    steps = 0
    current = csp
    for i in range(max_steps):
        if sum(map(lambda x: len(x), csp['edges'])) == 0:
            print("Steps used:", steps)
            return current
        # print("initial edges:", csp['edges'])
        queens = degree_compare(current['edges'], compare='greatest')
        queen = random.choice(queens)
        # print("queen to move", queen)
        find_minimum(queen, current)
        # print("new edges", csp['edges'])
        steps += 1

    return False


def find_minimum(column, csp):
    board_size = len(csp['vertices'])
    row = csp['vertices'][column]

    conflicts = generate_row_conflicts(column, csp, board_size)

    min_rows = degree_compare(conflicts)
    min_row = random.choice(min_rows)
    min_edge = conflicts[min_row]

    previous_edges = csp['edges'][column]

    csp['vertices'][column] = min_row
    csp['edges'][column] = min_edge

    fix_graph_integrity(column, previous_edges, min_edge, csp)


def does_conflict(queen1_position, queen2_position):

    # Consider 4 diagonals
    x_difference = abs(queen1_position[1] - queen2_position[1])
    y_difference = abs(queen1_position[0] - queen2_position[0])

    return x_difference == y_difference or \
        queen1_position[0] == queen2_position[0]


'''

'''


def generate_row_conflicts(column, csp, board_size):

    # Build list of conflicts on rows
    conflicts = [set() for _ in range(board_size)]

    # Get miniumum rows
    for queen in range(len(csp['vertices'])):
        if queen == column:
            continue

        queen_row = csp['vertices'][queen]
        queen_column = queen

        # A queen conflicts with a row
        conflicts[queen_row].add(queen_column)

        column_difference = abs(column - queen_column)

        up_diagonal_row = queen_row - column_difference
        down_diagonal_row = queen_row + column_difference

        if up_diagonal_row >= 0:
            conflicts[up_diagonal_row].add(queen_column)

        if down_diagonal_row < board_size:
            conflicts[down_diagonal_row].add(queen_column)
    return conflicts


'''
    Fix the edges of a graph given the vertex changed, previous and new_edge set

    vertex: Index of the vertex that was changed to have new edges
    previous_edges: set of edges before the new assignments
    new_edges: set of edges after the new assignment
    graph: Graph structure to alter

    Result: Alters graph such that edges properly reflect the new_edges. 
'''


def fix_graph_integrity(vertex, previous_edges, new_edges, graph):

    for queen_to_fix in previous_edges:
        if queen_to_fix not in new_edges:
            graph['edges'][queen_to_fix].remove(vertex)

    for queen_to_add in new_edges:
        if queen_to_add not in previous_edges:
            graph['edges'][queen_to_add].add(vertex)


'''
    Given a function 'compare', return the best value for edges.
    edges: a list of lists (or sets). edges[i] are the edges for vertex i
    compare: a function that takes to_compare_edges, current_best_edges as arguments. 
            When true, to_compare_edges becomes the best.

    return: vertex for the best based on compare
'''


def degree_compare(edges, compare="smallest"):

    best_vertices = [0]
    best_edges_length = len(edges[0])

    for vertex in range(1, len(edges)):
        length = len(edges[vertex])

        if length == best_edges_length:
            best_vertices.append(vertex)
            continue

        if compare == 'smallest':
            if length < best_edges_length:
                best_vertices = [vertex]
                best_edges_length = length
        else:
            if length > best_edges_length:
                best_vertices = [vertex]
                best_edges_length = length

    return best_vertices
