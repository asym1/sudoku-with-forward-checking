import sys, pygame as pg
import numpy as np
from copy import deepcopy

# Global Variables
solvedPuzzle = None # storing correct answer if found
numOfBacktracks = 0 # number of backtracks for a statistical analysis later

## All Helper Functions
# Function to store the solved puzzle if found
def found_solved(solved):
    global solvedPuzzle
    solvedPuzzle = solved

# Removes value from all other domains & ensures no domain is empty
def forward_checking(curDomain, value, row, column):
    # copying the arrays so i don't change the global list & mess with the backtracking
    domainCopy = deepcopy(curDomain) # deep copy so lists get copied as well not just dictionary keys

    # Remove value from all other domains in the row/column and returns false if no legal values left in a domain
    for i in range(9):
        if i == column:
            continue
        if value in domainCopy[(row, i)]: domainCopy[(row, i)].remove(value)
        if len(domainCopy[(row, i)]) == 0:
            return True, domainCopy
    for i in range(9):
        if i == row:
            continue
        if value in domainCopy[(i, column)]: domainCopy[(i, column)].remove(value)
        if len(domainCopy[(i, column)]) == 0:
            return True, domainCopy

    # Check the local 3x3 using modulo to remove the values from there too
    startX = row - (row % 3)
    startY = column - (column % 3)
    for i in range(3):
        for j in range(3):
            curRow = startX + i
            curCol = startY + j
            if curRow == row and curCol == column:
                continue
            if value in domainCopy[(curRow, curCol)]: domainCopy[(curRow, curCol)].remove(value)
            if len(domainCopy[(curRow, curCol)]) == 0:
                return True, domainCopy

    return False, domainCopy

def solve_sodoku(curPuzzle, curDomains, row, column, viz=None):
    global numOfBacktracks

    # Puzzle solved
    if (row == 8) and (column == 9):
        found_solved(curPuzzle)
        if viz: viz.draw("Solved!")
        return True

    # Move to next row
    if column == 9:
        row += 1
        column = 0

    # Skip pre-filled cell
    if curPuzzle[row][column] != '0':
        return solve_sodoku(curPuzzle, curDomains, row, column+1, viz)

    # Try all numbers in domain
    for num in list(curDomains[(row, column)]):
        curPuzzle[row][column] = num
        isEmptyDomain, newDomain = forward_checking(curDomains, str(num), row, column)

        if not isEmptyDomain:
            if viz:  # draw assignment
                viz.puzzle[row][column] = num
                viz.draw("Solving...")

            if solve_sodoku(curPuzzle, newDomain, row, column+1, viz):
                return True

        # Undo assignment (backtrack)
        curPuzzle[row][column] = '0'
        numOfBacktracks += 1
        if viz: 
            viz.puzzle[row][column] = '0'
            viz.increase_backtracks()

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
defaultDomain = ['1','2','3','4','5','6','7','8','9']
domains = {(i,j): list(defaultDomain) for i in range(9) for j in range(9)} # using list(domain) to create new list each time

# start by forward checking on the cells that already have values (hints) to that we start backtracking with domains
# that already account for the constraints applied by the hints
for i in range(9):
    for j in range(9):
        if inputPuzzle[i][j] != '0':
            incorrect, domains = forward_checking(domains, inputPuzzle[i][j], i, j)
            if incorrect:
                print("INITIAL PUZZLE INCORRECT!")
                exit(0)

## this funtion is a safe way to read the sodoku pizzle from the txt file and convert it to the 9x9 format. 
def load_input():
    try:
        ##Tries to open the file and reads the contents as a string. 
        with open("input.txt", "r") as f:
            s = f.read().strip() 
    except FileNotFoundError:
        print("PLEASE MAKE SURE input.txt EXISTS")
        sys.exit(1)

#goes through file content and will keep digits from 1-9 
    chars = [ch for ch in s if ch.isdigit()] 
    if len(chars) < 81:
        print("NOT ENOUGH CELLS INPUTTED FOR A 9x9")
        sys.exit(1)

    return np.array(chars[:81]).reshape(9, 9)

# Start Backtracking
attempt = solve_sodoku(inputPuzzle, domains, 0, 0)
if attempt:
    print("SOLUTION FOUND")
    print(f"NUM OF BACKTRACKS: {numOfBacktracks}")
    print(solvedPuzzle)
else:
    print("THIS IS IMPOSSIBLE!!!") 