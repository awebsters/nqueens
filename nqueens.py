
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


'''
This function finds a solution to the board_size-queen problem
'''


def solve(board_size):

    csp = initialize(board_size)

    max_steps = board_size
    if board_size < 1000:
        max_steps = 200
    elif board_size < 10000:
        max_steps = 500
    elif board_size < 100000:
        max_steps = 1000
    else:
        max_steps = 1500

    # We keep looping until we find a solution
    while True:

        # Use min-conflicts on our initialization
        result = min_conflicts(csp, max_steps)
        if result:
            break

        # If failed, then try with new initialization
        csp = initialize(board_size)

    # We created with 0 based indexes, the output required 1 based.
    answer = [i + 1 for i in csp['queens']]
    return answer


'''
Function for greedy initialization. Returns csp problems defined at header for file
'''


def initialize(board_size):

    csp = {'queens': [], 'row_conflicts': [0] * board_size,
           'diagonal_forward_conflicts': [0] * (2 * board_size - 1),
           'diagonal_backward_conflicts': [0] * (2 * board_size - 1)}

    # List of all empty rows, initially all rows are empty
    # We randomize this list so we are picking investigating rows at random for possibilities of 0 conflict

    empty_rows = list(range(board_size))
    random.shuffle(empty_rows)

    # Add queens one at the time in the best position
    # The idea behind this is to only consider rows in the empty_rows column. This has a new benefits:
    # We consider rows in a random order because it is shuffled, this allows re-initialization to be helpful
    # We automatically place things so there are no conflicts along rows or columns
    # It greatly increases the chances of finding a random row with 0 conflicts quickly. This really helps complexity

    for column in range(board_size):

        insert_best_row(column, csp, board_size, empty_rows)

    return csp


'''
Edits csp to add the best row for a queen in column <column> under the current state of the csp problem
It only returns a row in the empty_row list for efficiency reason (this means we are not wasting compute on rows with queens)
'''


def insert_best_row(column, csp, board_size, empty_rows):

    best_row = -1
    smallest_conflict = board_size
    empty_row_index = -1

    for index in range(len(empty_rows)):
        row = empty_rows[index]

        # We know no other queen is in this row, however lets check for diagonal attacks

        conflicts = csp['diagonal_forward_conflicts'][column + board_size - 1 - row]
        conflicts += csp['diagonal_backward_conflicts'][column + row]

        # If we have no conflicts we have found a good row
        if conflicts == 0:

            # This is no longer an empty_row
            del empty_rows[index]

            append_queen(row, csp, board_size)
            return

        # Keep track of the row with the fewest conflicts just in case we dont find a perfect one
        if conflicts < smallest_conflict:
            smallest_conflict = conflicts
            best_row = row
            empty_row_index = index

    # If no 0 conflicting row was found, use the minimum
    del empty_rows[empty_row_index]
    append_queen(best_row, csp, board_size)


'''
Appends a queen to the csp problem. This makes necessary changes to all conflict structures in csp
'''


def append_queen(row, csp, board_size):
    column = len(csp['queens'])

    csp['queens'].append(row)
    csp['row_conflicts'][row] += 1
    csp['diagonal_forward_conflicts'][column + board_size - 1 - row] += 1
    csp['diagonal_backward_conflicts'][column + row] += 1


'''
This function attempts to find a board solution by slowly minimizing the conflicts.
On each step it will: 
    Choose the most conflict queen in csp
    Choose the row in its column with the minimum conflicts
    
With the correct initialization on csp, this function will each a global minimum of 0 conflicts.
Poor initializations will result in local minimums.
'''


def min_conflicts(csp, max_steps):
    board_size = len(csp['queens'])

    steps = 0
    current = csp
    for i in range(max_steps):
        if is_solution(current):
            print("steps:", steps)
            return current

        # Get the most conflicted queen column
        queen = get_most_conflicted(current, board_size)

        # change it to the minumum row
        insert_minimum(queen, current, board_size)
        steps += 1

    return False


'''
Check if csp is a solution, return the result
'''


def is_solution(csp):

    # we need to go through all attack "vectors" and check if more then 1 queen can attack on this vector

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


'''
Get the column for the queen with the most conflicts currently in csp
'''


def get_most_conflicted(csp, board_size):

    # We store all of the current minimum so we can randomly pick one of the options
    # This is done because the algorithm has no way to quickly assign a further cost to any row with 0 value
    # So one must be chosen randomly

    queens = []
    maximum_conflicts = -1

    for column in range(len(csp['queens'])):
        row = csp['queens'][column]

        # Calculate the number of queens that can attack
        # Remember this queen is registered on all of its possible attacking vectors so we subtract 1

        conflicts = csp['row_conflicts'][row] - 1
        conflicts += csp['diagonal_forward_conflicts'][column + board_size - 1 - row] - 1
        conflicts += csp['diagonal_backward_conflicts'][column + row] - 1

        # When we have the same conflict add to list of known smallest, else reset the minimum data to this queen
        if conflicts == maximum_conflicts:
            queens.append(column)
        elif conflicts > maximum_conflicts:
            maximum_conflicts = conflicts
            queens = [column]

    return random.choice(queens)


'''
Given a csp and a column, change its row to the row with minimum conflicts in its column.
'''


def insert_minimum(column, csp, board_size):

    conflicts = smallest_row_conflicts(column, csp, board_size)
    row = random.choice(conflicts)

    previous_row = csp['queens'][column]

    # Add new queen and update attack vectors
    csp['queens'][column] = row
    csp['row_conflicts'][row] += 1
    csp['diagonal_forward_conflicts'][column + board_size - 1 - row] += 1
    csp['diagonal_backward_conflicts'][column + row] += 1

    # Remove conflicts related to previous position to keep structure integrity
    csp['row_conflicts'][previous_row] -= 1
    csp['diagonal_forward_conflicts'][column + board_size - 1 - previous_row] -= 1
    csp['diagonal_backward_conflicts'][column + previous_row] -= 1


'''
From a column and a csp, get a list of all the smallest conflicting rows in that column
'''


def smallest_row_conflicts(column, csp, board_size):

    # Same concept as in get_most_conflicted
    smallest_rows = []
    smallest_conflicts = board_size

    for row in range(board_size):

        # Calculate what the conflict would be for this position
        row_conflicts = 0
        row_conflicts += csp['row_conflicts'][row]
        row_conflicts += csp['diagonal_forward_conflicts'][column + board_size - 1 - row]
        row_conflicts += csp['diagonal_backward_conflicts'][column + row]

        if row_conflicts == smallest_conflicts:
            smallest_rows.append(row)

        elif row_conflicts < smallest_conflicts:
            smallest_rows = [row]
            smallest_conflicts = row_conflicts

    return smallest_rows
