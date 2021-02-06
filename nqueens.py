
import random


# Implement a solver that returns a list of queen's locations
#  - Make sure the list is the right length, and uses the numbers from 0 .. BOARD_SIZE-1

def initialize(board_size):
    csp = {'vertices': [], 'edges': [], 'empty_edges': 0}

    vertices = list(range(1, board_size+1))
    random.shuffle(vertices)
    csp['vertices'] = vertices

    for vertex in range(len(vertices)):
        vertex_1 = (csp['vertices'][vertex], vertex)

        edges = []

        for check_vertex in range(len(vertices)):
            vertex_2 = (csp['vertices'][check_vertex], check_vertex)

            if vertex == check_vertex:
                continue
            elif does_conflict(vertex_1, vertex_2):
                edges.append(check_vertex)
        if not edges:
            csp['empty_edges'] += 1

        csp['edges'].append(edges)

    return csp


def solve(board_size):

    # This almost certainly is a wrong answer!
    answer = initialize(board_size)
    while True:
        result = min_conflicts(answer, (board_size ** 2)//2)
        if result:
            break
        answer = initialize(board_size)

    return answer['vertices']


def min_conflicts(csp, max_steps):

    current = csp
    for i in range(max_steps):
        if current['empty_edges'] == 0:
            return current
        queen = min_degree(current['edges'])
        find_minimum(queen, current)
        # current[queen] = value
    return False


def min_degree(edges):

    min_vertex = 0
    min_degree = len(edges[min_vertex])

    for vertex in range(1, len(edges)):
        degree = len(edges[vertex])
        if degree < min_degree:
            min_vertex = vertex
            min_degree = degree

    return min_vertex


def find_minimum(vertex, csp):
    board_size = len(csp['vertices'])

    min_vertex_value = csp['vertices'][vertex]
    min_edges = csp['edges'][vertex]

    for row in range(board_size):

        edges = get_edges(row, csp)

        if len(edges) < len(min_edges):
            min_vertex_value = row
            min_edges = edges

    if len(min_edges) == 0 and len(csp['edges'][vertex]) != 0:
        csp['empty_edges'] -= 1

    csp['vertices'][vertex] = min_vertex_value
    csp['edges'][vertex] = min_edges

    return min_vertex_value


def get_edges(vertex, csp):
    edges = []

    vertex = (csp['vertices'][vertex], vertex)

    for check_vertex in range(len(csp['vertices'])):
        if vertex == check_vertex:
            continue

        vertex_2 = (csp['vertices'][check_vertex], check_vertex)

        if does_conflict(vertex, vertex_2):
            edges.append(check_vertex)

    return edges


def does_conflict(queen1_position, queen2_position):

    # Consider 4 diagonals
    x_difference = abs(queen1_position[1] - queen2_position[1])
    y_difference = abs(queen1_position[0] - queen2_position[0])

    return x_difference == y_difference or \
        queen1_position[0] == queen2_position[0]
