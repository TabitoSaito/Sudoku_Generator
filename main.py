import numpy as np
from sudoku_gen import SudokuGen

test_array = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [6, 9, 8, 7, 5, 0, 4, 3, 1],
                       [2, 5, 3, 4, 4, 4, 3, 3, 3],

                       [4, 4, 4, 4, 4, 5, 4, 4, 4],
                       [0, 5, 1, 5, 1, 0, 5, 5, 5],
                       [5, 6, 6, 6, 6, 6, 6, 6, 6],

                       [7, 7, 7, 7, 7, 7, 7, 7, 7],
                       [8, 8, 8, 8, 8, 8, 8, 8, 8],
                       [9, 9, 9, 9, 9, 9, 9, 9, 9]])

test_array_sudoku = np.array([[0, 0, 0, 8, 0, 1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 4, 3],
                             [5, 0, 0, 0, 0, 0, 0, 0, 0],

                             [0, 0, 0, 0, 7, 0, 8, 0, 0],
                             [0, 0, 0, 0, 0, 0, 1, 0, 0],
                             [0, 2, 0, 0, 3, 0, 0, 0, 0],

                             [6, 0, 0, 0, 0, 0, 0, 7, 5],
                             [0, 0, 3, 4, 0, 0, 0, 0, 0],
                             [0, 0, 0, 2, 0, 0, 6, 0, 0]])

gen = SudokuGen()
#
#
# sudoku = gen.gen_sudoku()
# gen.solve(sudoku)
# gen.sudoku_print(sudoku)
#
# gen.sudoku_print(test_array_sudoku)

gen.solve(test_array_sudoku)

# test_3d = np.zeros((3, 10, 5))
#
# print(test_3d)

# gen.test(test_array_sudoku)

# print(test_array_sudoku[:, 0])

# test2 = test_array_sudoku[0].copy()
#
# print((test2 == test_array_sudoku).all())

# gen.soft_solve(test_array_sudoku)
# gen.sudoku_print(gen.array)
