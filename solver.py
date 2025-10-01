import numpy as np

# Global Variables
solvedPuzzle = None # storing correct answer if found
numOfBacktracks = 0 # number of backtracks for a statistical analysis later

## All Helper Functions

# Function to print the solved puzzle instead of doing it in main function
def found_solved(solved):
    global solvedPuzzle
    solvedPuzzle = solved

# returns a true/false for failing (found an empty domain) the new domain after forward checking
def forward_checking(curPuzzle, curDomains, value, row, column):
    # copying the arrays so i don't change the global list & mess with the backtracking
    curPuzzle = curPuzzle.copy()
    curDomains = curDomains.copy()


    return True, curDomains

def solve_sodoku(curPuzzle, curDomains, row, column):
    if (row == 8) and (column == 9):
        found_solved(curPuzzle)
        return True
    if column == 9:
        row +=1
        column = 0
    if curPuzzle[row][column] != '.':
        return solve_sodoku(curPuzzle, curDomains, row, column+1)
    for num in curDomains[(row, column)]:
        curPuzzle[row][column] = str(num)
        isEmptyDomain, newDomain = forward_checking(curPuzzle, curDomains, num, row, column)
        if(isEmptyDomain):
            curPuzzle[row][column] = '.'
            continue
        if solve_sodoku(curPuzzle, newDomain, row, column + 1):
            return True
        curPuzzle[row][column] = '.'
    return False


# connecting and reading the file
try:
    f = open('input.txt', 'r')
    inputPuzzle = f.read()
    f.close()
except FileNotFoundError:
    print("PLEASE MAKE SURE INPUT.TXT EXISTS")
    exit(0)

# store input values in ndarray and reshape it so it fits the dimensions
inputPuzzle = np.array(list(inputPuzzle))
try:
    inputPuzzle = inputPuzzle.reshape(9,9)
except ValueError:
    print("NOT ENOUGH CELLS INPUTTED FOR A 9x9")
    exit(0)
print(inputPuzzle)

# create Dictionary that stores the domain of every cell (Using Dictionary Comprehension)
defaultDomain = [1,2,3,4,5,6,7,8,9]
domains = {(i,j): defaultDomain for i in range(9) for j in range(9)}

# start by forward checking on the cells that already have values (hints) to that we start backtracking with domains
# that already account for the constraints applied by the hints
for i in range(9):
    for j in range(9):
        if inputPuzzle[i][j] != '.':
            _, domains = forward_checking(inputPuzzle, domains, inputPuzzle[i][j], i, j)

# Start Backtracking
attempt = solve_sodoku(inputPuzzle, domains, 0, 0)
if attempt:
    print(solvedPuzzle)
else:
    print("THIS IS IMPOSSIBLE YOU SCUMBAG!!!")