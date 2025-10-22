# sudoku-with-forward-checking
A 9x9 sudoku solver that uses the forward checking technique for enforcing constraints using domain reduction instead of bruteforce
## Intro
- A regular backtracking algorithm takes all possible paths for one variable, checks if current puzzle is legal, and if it is, moves on to the next cell & does the same thing.
- Forward checking involves creating a domain of all legal moves (so that only they can be chosen as candidates for backtracking), and everytime a value is chosen for a cell, the domains of the cells in the respective column, row, and subgrid get that value removed as it's no longer a legal move.
- This ensures that if a cell has no legal moves left, we can figure it out early and avoid a path that will eventually fail
## Implementation
- `input.txt` is used for inputting the initial puzzle string, while leaving unfilled values as zeros
- `solver.py` is the Text UI based solver that shows the solution with it's true speed, and gives the final puzzle with the number of backtracks as well
- `gui_solver.py` is the GUI solver that shows the process of solving, slowed down to show steps. You can see the number of backtracks live & all the paths the algorithm goes down before reaching the final solution
## How to use
- Simply plug the 9*9 puzzle as a string with '0' for unfilled values in `input.txt` & then run the script for the terminal or GUI