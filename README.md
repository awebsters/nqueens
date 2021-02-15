# N-Queens

Using an iterative repair method, this is a solution to the n-queens problem defined below.

**The solution is further described in `technical.pdf`**

## Problem Definition

Given an integer, n where 4 <= n <= 1,000,000, find a way to place n queens on a board of size nxn such that no two queens can attack each other.

The `run.py` file will read from `nqueens.txt` for inputs

**Input File**:

```
4
5
6
```

**Output**:

```
$ python3 run.py nqueens.txt
[3, 1, 4, 2]
[3, 1, 4, 2, 5]
[2, 4, 6, 1, 3, 5]
$
```

The output format is:

list[column] = row
