
#################################
#
#  NOTE: Do not edit this file.
#

import sys

from nqueens import solve

if len(sys.argv) != 2:
    print("\n\tUsage: python3 run.py <test-file>\n")
    exit(1)

in_file = sys.argv[1]

problems = []

with open(in_file) as f:
    problems = map(int, f.readlines())


def print_answer(solve):
    for row in range(len(solve)):
        for col in range(len(solve)):
            print('Q' if solve[col] == row + 1 else '_', end=" ")
        print("")


for p in problems:
    answer = solve(p)
    print(answer)
    # print_answer(answer)
    print("\n")