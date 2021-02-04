# a1-nqueens

Assignment 1: N-Queens Problem

## Input

Your program will read input from a file called `nqueens.txt` which contains several lines of input. Each line of input consists of a single integer value, n, where n > 3 and n <= 10,000,000, that determines the size of the n-queens problem to be solved. For instance, line 1 of a sample “nqueens.txt” input file could contain the integer value “128”. This means that you need to solve the problem for 128 queens on a 128x128 size chessboard. Each successive line of input contains a new integer value that determines the size of the problem to solve.

## Output

Your program will write to the terminal: one printed list per problem. Output consists of successive 1-based matrices (i.e., the queen in the first row would use index 1, not 0) containing the position of each queen. The formatting of the output should be in lists printed from Python, as seen in the example below:

### Input/Output Formatting Example

**Input File**:
```
4
5
6
7
8
9
10
```

**Output**:
```
$ python3 run.py nqueens.txt
[3, 1, 4, 2]
[3, 1, 4, 2, 5]
[2, 4, 6, 1, 3, 5]
[2, 5, 1, 4, 7, 3, 6]
[4, 7, 3, 8, 2, 5, 1, 6]
[4, 6, 3, 9, 7, 1, 8, 2, 5]
[6, 3, 5, 2, 8, 10, 7, 4, 1, 9]
$
```

## Skeleton Code

The `run.py` file *should not be editted* -- it exists to parse the input file and output the solutions for you. Instead, you should modify `nqueens.py` so that the `solve(..)` method returns a solution. By default, it returns a properly formatted random list of integers.

## Grading

The marking of this assignment will be done in two parts. The first part is based on the correctness and efficiency of your team’s code. The second part is a written technical document.

The first part is out of 9 points. A text file will be read into your code containing a list of numbers. Each line of input consists of a single integer value, n, where n > 3 and n <= 10,000,000, that determines the size of the n-queens problem to be solved. For each integer value in the file, the output must have a corresponding list containing the correct values in the formatting outlined above. If formatting instructions are not followed, marks will be deducted. If the submitted code does not compile and/or run incorrectly or if the runtime of the code exceeds 30 minutes, you will not receive a grade for the problematic board sizes. Please see the full assignment document for further details on grading this component.

The second part is a grade on your technical document describing your algorithm. This is worth 3 points. The grade will include grammar, spelling, presentation quality, and the description of your algorithms. I should be able to know how your algorithms work from reading the document. There is no word count, however, please be concise and aim to write no more than two pages. Regarding presentation quality, do not submit a .txt file. The document should be presented as nicely as possible, with headings where appropriate. Put the name and student IDs of all group members on this document. Convert the file to a PDF and name it nqueens.pdf.

This assignment is 12% of your total grade for the course.

Submit the program and technical document, one per group, compressed together in a .zip file named nqueens.zip to the onQ Assignment 1 Dropbox.
