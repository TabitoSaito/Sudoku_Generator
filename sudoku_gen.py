import collections
import random
import numpy as np
import math
import os
import time
import sys


class SudokuGen:

    def __init__(self, size=9, difficulty="easy", show_solution=True, delay=False):
        self.size = size
        self.array = []
        self.riddle = []
        self._calc_box_size()
        self._phantom_array = []
        self.difficulty = difficulty
        self.solution = show_solution
        self._recursion_limit()
        self.delay = delay
        self.delay_time = 0.1

    def gen_empty_field(self):
        array = []
        row = []
        for i in range(0, self.size):
            row.append(0)
        for j in range(0, self.size):
            array.append(row)

        self.riddle = np.array(array)
        self.array = np.array(array)
        self._gen_phantom_array()

    def _gen_phantom_array(self):
        self._phantom_array = []
        row = []
        for i in range(0, self.size):
            z_list = []
            for z in range(0, self.size):
                z_list.append(0)
            row.append(z_list)
        for j in range(0, self.size):
            self._phantom_array.append(row)
        self._phantom_array = np.array(self._phantom_array)

    def _calc_box_size(self):
        self._box = self.size**0.5

    def _quadrant_index(self, row, col):
        quadrant = math.ceil((row + 1) / self._box)
        index_top = int(quadrant * self._box)
        index_bot = int(index_top - self._box)
        quadrant = math.ceil((col + 1) / self._box)
        index_left = int(quadrant * self._box)
        index_right = int(index_left - self._box)
        return index_top, index_bot, index_left, index_right

    def _gen_solution(self, i_row=0, i_col=0):
        if self._test_finish():
            if self.solution:
                self.clear()
                # print(f"{self.array}\n")
                self.sudoku_print(self.array)
        else:
            if self.solution:
                self.clear()
                # print(f"{self.array}\n")
                self.sudoku_print(self.array)
                if self.delay:
                    time.sleep(self.delay_time)
            possible_n = []
            for n in range(1, self.size + 1):
                if self._test_rules(i_row, i_col, n):
                    possible_n.append(n)
                else:
                    possible_n.append(0)
            if possible_n.count(0) == self.size:
                self._go_back(i_row, i_col)
            else:
                n_choice = random.choice([x for x in possible_n if x != 0])
                possible_n.remove(n_choice)
                possible_n.append(0)

                self.array[i_row][i_col] = n_choice
                self._phantom_array[:, i_row, i_col] = possible_n
                if self._test_finish():
                    self._gen_solution()
                else:
                    self._go_forward(i_row, i_col)

    def _test_rules(self, row, col, n):
        quadrant = self._quadrant_index(row, col)
        if n in self.array[row]:
            # print("False because row")
            return False
        elif n in self.array[:, col:(col + 1)]:
            # print("False because col")
            return False
        elif n in self.array[quadrant[1]:quadrant[0], quadrant[3]:quadrant[2]]:
            # print("False because quart")
            return False
        return True

    def clear(self):
        os.system("cls")

    def _go_back(self, row, col):
        cell = self._phantom_array[:, row, col].copy()
        if (self.size + 1) not in cell:
            self.array[row][col] = 0
        if col == 0:
            col = 8
            row -= 1
        else:
            col -= 1

        cell = self._phantom_array[:, row, col].copy()
        if (self.size + 1) in cell:
            self._go_back(row, col)
        else:
            if (self.size + 1) not in cell:
                if collections.Counter(cell)[0] == self.size:
                    self._go_back(row, col)
                else:
                    n_choice = random.choice([x for x in cell if x != 0])
                    cell[cell == n_choice] = 0
                    self.array[row][col] = n_choice
                    self._phantom_array[:, row, col] = cell
                    self._go_forward(row, col)
            else:
                self._go_back(row, col)


    def _go_forward(self, row, col):
        if col == 8:
            col = 0
            row += 1
        else:
            col += 1

        if self.array[row][col] != 0:
            self._phantom_array[:, row, col] = [self.size + 1 for x in range(0, self.size)]
            self._go_forward(row, col)
        else:
            self._gen_solution(row, col)

    def _test_finish(self):
        if 0 in self.array:
            return False
        else:
            return True

    def _gen_riddle(self):
        choices = []
        if self.difficulty.lower() == "easy":
            sample = random.randint(int(self._box * 4), int(self._box * 5))
        elif self.difficulty.lower() == "normal":
            sample = random.randint(int(self._box * 3), int(self._box * 4))
        elif self.difficulty.lower() == "hard":
            sample = random.randint(int(self._box * 2), int(self._box * 3))
        else:
            sample = random.randint(int(self._box * 4), int(self._box * 5))

        while len(choices) != sample:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)

            if (row, col) not in choices:
                choices.append((row, col))

        for t in choices:
            self.riddle[t[0]][t[1]] = self.array[t[0]][t[1]]
        self.sudoku_print(self.riddle)

    def _recursion_limit(self):
        sys.setrecursionlimit(10000)

    def sudoku_print(self, array):
        print("\n")
        for i in range(0, len(array)):
            row = ""
            for j in range(0, len(array)):
                if (j + 1) % self._box == 0:
                    if j + 1 != self.size:
                        row += f" {array[i][j]} "
                        row += "|"
                    else:
                        row += f" {array[i][j]} "
                else:
                    row += f" {array[i][j]} "
            print(row)
            if (i + 1) % self._box == 0:
                if (i + 1) != self.size:
                    print("----------------------------")

    def solve(self, array):
        self.array = array.copy()
        self._gen_phantom_array()
        self._gen_solution()

    def gen_sudoku(self):
        self.gen_empty_field()
        self._gen_solution()
        self._gen_riddle()
        return self.riddle.copy()
