
import random

'''

CSP contains 4 aspects:

'queens' is a list of integers from [0 - n). The index represents the column whereas the value is the row of a queen

The other 3 aspects are too keep track of conflicts on different board dimensions, as we are guarantee no Queen
is placed on the same column we do not need to consider this dimension.

'row_conflicts': is a list of integers from [0 - n). The index represents the row whereas the value is the current
                number of queens that can attack on that row.

'diagonal_forward_conflicts': is a list of integers from [0 - 2*n-3). The index represents a forward diagonal and the
                            value represents how many queens can attack on that diagonal

This is a representation of a simple board and its forward diagonals with indexes

  0 1 2 3 4
0 4 5 6 7 8
1 3 4 5 6 7
2 2 3 4 5 6
3 1 2 3 4 5
4 0 1 2 3 4

'diagonal_backwards_conflicts': is a list of integers from [0 - 2*n-3). The index represents a forward diagonal and the
                            value represents how many queens can attack on that diagonal
  0 1 2 3 4
0 0 1 2 3 4
1 1 2 3 4 5
2 2 3 4 5 6
3 3 4 5 6 7
4 4 5 6 7 8

'''


def initialize(board_size):

    csp = {'queens': list(range(board_size)), 'row_conflicts': [0] * board_size,
           'diagonal_forward_conflicts': [0] * (2 * board_size - 1),
           'diagonal_backward_conflicts': [0] * (2 * board_size - 1)}

    random.shuffle(csp['queens'])

    queen_position = random.randint(0, board_size - 1)
    append_queen(queen_position, csp, board_size)

    for column in range(1, board_size):

        row = get_smallest_conflicts(column, csp, board_size)

        append_queen(row, csp, board_size)

    return csp


def get_smallest_conflicts(column, csp, board_size):

    smallest_rows = []
    smallest_conflicts = board_size

    for row in range(board_size):
        row_conflicts = 0

        row_conflicts += csp['row_conflicts'][row]

        row_conflicts += csp['diagonal_forward_conflicts'][column + board_size - 1 - row]

        row_conflicts += csp['diagonal_backward_conflicts'][column + row]

        if row_conflicts == smallest_conflicts:
            smallest_rows.append(row)
        elif row_conflicts < smallest_conflicts:
            smallest_rows = [row]
            smallest_conflicts = row_conflicts

    return random.choice(smallest_rows)


def solve(board_size):

    csp = initialize(board_size)
    while True:
        result = min_conflicts(csp, board_size)
        if result:
            break
        csp = initialize(board_size)

    return csp['queens']


def print_answer(solve):
    for row in range(len(solve)):
        for col in range(len(solve)):
            print 'Q ' if solve[col] == row else '_ ',
        print("")


def min_conflicts(csp, max_steps):
    board_size = len(csp['queens'])

    steps = 0
    # print_answer(csp['queens'])
    current = csp
    for i in range(max_steps):
        if is_solution(current):
            print("Steps used:", steps)
            return current

        queen = get_most_conflicted(current, board_size)
        insert_minimum(queen, current, board_size)
        # [4, 2, 0, 3, 1]
        # print_answer(csp['queens'])
        steps += 1

    return False


def get_most_conflicted(csp, board_size):

    queens = []
    maximum_conflicts = -1

    for column in range(len(csp['queens'])):
        row = csp['queens'][column]

        conflicts = csp['row_conflicts'][row] - 1
        conflicts += csp['diagonal_forward_conflicts'][column + board_size - 1 - row] - 1
        conflicts += csp['diagonal_backward_conflicts'][column + row] - 1

        if conflicts == maximum_conflicts:
            queens.append(column)
        elif conflicts > maximum_conflicts:
            maximum_conflicts = conflicts
            queens = [column]

    return random.choice(queens)


def is_solution(csp):

    for conflicts in csp['row_conflicts']:
        if conflicts > 1:
            return False

    for conflicts in csp['diagonal_forward_conflicts']:
        if conflicts > 1:
            return False

    for conflicts in csp['diagonal_backward_conflicts']:
        if conflicts > 1:
            return False

    return True


def insert_minimum(column, csp, board_size):

    conflicts = generate_conflicts(column, csp, board_size)

    min_rows = all_smallest(conflicts)
    row = random.choice(min_rows)

    previous_row = csp['queens'][column]

    # Add new queen
    csp['queens'][column] = row
    csp['row_conflicts'][row] += 1
    csp['diagonal_forward_conflicts'][column + board_size - 1 - row] += 1
    csp['diagonal_backward_conflicts'][column + row] += 1

    # Remove conflicts related to previous position
    csp['row_conflicts'][previous_row] -= 1
    csp['diagonal_forward_conflicts'][column + board_size - 1 - previous_row] -= 1
    csp['diagonal_backward_conflicts'][column + previous_row] -= 1


def generate_conflicts(column, csp, board_size):

    conflicts = []

    for row in range(board_size):

        row_conflicts = 0

        row_conflicts += csp['row_conflicts'][row]

        row_conflicts += csp['diagonal_forward_conflicts'][column + board_size - 1 - row]

        row_conflicts += csp['diagonal_backward_conflicts'][column + row]

        conflicts.append(row_conflicts)

    return conflicts


def append_queen(row, csp, board_size):
    column = len(csp['queens'])

    csp['queens'].append(row)
    csp['row_conflicts'][row] += 1
    csp['diagonal_forward_conflicts'][column + board_size - 1 - row] += 1
    csp['diagonal_backward_conflicts'][column + row] += 1


def all_smallest(data):

    best_indexes = [0]
    best_value = data[0]

    for index in range(1, len(data)):

        if best_value == data[index]:
            best_indexes.append(index)
            continue

        if data[index] < best_value:
            best_indexes = [index]
            best_value = data[index]

    return best_indexes
