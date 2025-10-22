# Imported Packages & Modules
import pygame as pg
import sys
import numpy as np
import time
from solver import solve_sodoku, forward_checking, found_solved  # using my solver functions

# Global Variables
CELL = 60    # size of one square in pixels
GRID = 9     # 9x9 sudoku
W, H = CELL * GRID, CELL * GRID + 50   # screen dimensions, the 50 is added for extra space

class GuiSolver:
    ##Simple GUI class that uses pygame to show the sudoku being solved.
    # I separated this from the solver so the GUI is optional.
    def __init__(self, puzzle):
        pg.init()
        self.screen = pg.display.set_mode((W, H))
        pg.display.set_caption("Sodoku GUI Solver")
        # Fonts for numbers and info text- WE CAN CHANGE THIS TO OTHER FONTS
        self.font = pg.font.SysFont("couriernew", 34, bold=True)
        self.small = pg.font.SysFont("arial", 22, bold=True)

        self.puzzle = puzzle # Store puzzle (2D array of chars)
        self.backtracks = 0 # Track backtracks to show how many times we undo a move
        # Delay so solving isn’t instant (I useD time.sleep instead of pg delay)
        self.delay = 0.08

### not sure if like all of this part, 80% going to it edit again.
    def draw(self, status="Solving..."):

       # Draws the full sudoku board + grid + info bar.

        # Makes sure user can close window at any time
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Background color
        self.screen.fill((20, 20, 30))

        # Draws the 9x9 grid
        for r in range(GRID):
            for c in range(GRID):
                rect = pg.Rect(c*CELL, r*CELL, CELL, CELL)
                pg.draw.rect(self.screen, (50, 50, 60), rect, 1)
                if self.puzzle[r][c] != '0':
                    # All numbers shown in green
                    txt = self.font.render(str(self.puzzle[r][c]), True, (50, 255, 50))
                    self.screen.blit(txt, txt.get_rect(center=rect.center))

        # 3x3 lines to show sudoku sub-grids+ made them bold
        for i in range(0, GRID+1, 3):
            pg.draw.line(self.screen, (255, 255, 255), (0, i*CELL), (W, i*CELL), 3)
            pg.draw.line(self.screen, (255, 255, 255), (i*CELL, 0), (i*CELL, GRID*CELL), 3)

        # Info bar (backtracks + status)
        txt = self.small.render(f"Backtracks: {self.backtracks}", True, (50, 255, 50))
        self.screen.blit(txt, (10, H-40))
        txt2 = self.small.render(status, True, (50, 255, 50))
        self.screen.blit(txt2, (W-140, H-40))

        pg.display.flip()
        time.sleep(self.delay)   #  my own choice instead of pg.time.delay - ineffecient Im going to change this tommorow SARA REMEMBER !!1

    def increase_backtracks(self):
    ### Called whenever solver undoes a move.
        self.backtracks += 1
        self.draw("Backtracking...")

# Main
##The puzzle is stored in a txt file and has 81 digits. Here what is happeninng is that this will read the
#file as a string and turn it in to a 9x9 numpy array.
if __name__ == "__main__":

    # Load puzzle from file
    try:
        with open("input.txt", "r") as f:
            s = f.read().strip() # remove spaces or new lines to keep the puzzle digits
    except FileNotFoundError:
        print("PLEASE MAKE SURE input.txt EXISTS")
        sys.exit(0)

    # Convert puzzle into numpy array
    chars = [ch for ch in s if ch.isdigit()]
    if len(chars) < 81:
        print("NOT ENOUGH CELLS INPUTTED FOR A 9x9")
        sys.exit(1)
    inputPuzzle = np.array(chars[:81]).reshape(9, 9)

    # Initializes domains
    defaultDomain = ['1','2','3','4','5','6','7','8','9']
    domains = {(i, j): list(defaultDomain) for i in range(9) for j in range(9)}
    # Applies forward checking for all given hints
    for i in range(9):
        for j in range(9):
            if inputPuzzle[i][j] != '0':
                incorrect, domains = forward_checking(domains, inputPuzzle[i][j], i, j)
                if incorrect:
                    print("INITIAL PUZZLE INCORRECT!")
                    sys.exit(0)

    # Run GUI solver
    viz = GuiSolver(inputPuzzle.copy())
    viz.draw("Starting...")

    attempt = solve_sodoku(inputPuzzle, domains, 0, 0, viz)

    if attempt:
        print("SOLUTION FOUND")
        viz.draw("Solved!")
    else:
        print("THIS IS IMPOSSIBLE!!!")
        viz.draw("No solution")

    # Keep window open until closed
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()