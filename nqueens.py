
import random


# Implement a solver that returns a list of queen's locations
#  - Make sure the list is the right length, and uses the numbers from 0 .. BOARD_SIZE-1
def solve(board_size):

    # This almost certainly is a wrong answer!
    answer = list(range(1, board_size+1))
    answer = min_conflicts(answer, board_size**2)

    return answer


def min_conflicts(csp, max_steps):
    board_size = len(csp)

    current = csp
    for i in range(max_steps):
        if is_solution(current):
            return current
        queen = random.randint(0, board_size - 1)
        value = find_minimum(queen, current)
        current[queen] = value
    return False


def find_minimum(queen_index, board):
    board_size = len(board)

    minimum = None
    minimum_conflicts = board_size + 1

    board = board[:]
    del board[queen_index]

    for row in range(board_size):
        testing_position = (row, queen_index)
        conflicts = count_conflicts(testing_position, board)
        if conflicts < minimum_conflicts:
            minimum = row
            minimum_conflicts = conflicts
    return minimum


def is_solution(current):
    for i in range(len(current)):
        queen = (current[i], i)
        if count_conflicts(queen, current) != 0:
            return False
    return True


def count_conflicts(root_queen, all_queens):
    conflicts = 0

    for i in range(len(all_queens)):
        queen = (all_queens[i], i)
        if root_queen == queen:
            continue
        conflicts += int(does_conflict(root_queen, queen))

    return conflicts


def does_conflict(queen1_position, queen2_position):

    # Consider 4 diagonals
    x_difference = abs(queen1_position[1] - queen2_position[1])
    y_difference = abs(queen1_position[0] - queen2_position[0])

    return x_difference == y_difference or \
        queen1_position[1] == queen2_position[1] or \
        queen1_position[0] == queen2_position[0]
