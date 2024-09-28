import numpy as np
from sudoku_gen import SudokuGen

test = np.array([[1, 2, 1, 1, 1, 1, 1, 1, 1], [5, 2, 2, 2, 2, 2, 2, 2, 2], [3, 3, 3, 3, 3, 3, 3, 3, 3],
                 [4, 4, 4, 4, 4, 4, 4, 4, 4], [5, 5, 5, 5, 0, 5, 5, 5, 5], [6, 0, 0, 0, 0, 0, 0, 0, 0],
                 [7, 7, 7, 7, 7, 7, 7, 7, 7], [8, 8, 8, 8, 8, 8, 8, 8, 8], [9, 9, 9, 9, 9, 9, 9, 9, 9]])

gen = SudokuGen()


sudoku = gen.gen_sudoku()
gen.solve(sudoku)
gen.sudoku_print(sudoku)
