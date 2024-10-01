import collections
import random
import numpy as np
import math
import os
import time
import sys


def clear() -> None:
    os.system("cls")


class SudokuGen:

    def __init__(self, size: int = 9, difficulty: str = "easy", show_process: bool = False, delay: bool = False) -> None:
        self._size: int = size
        self.array: np.ndarray = self.gen_empty_array()
        self.riddle: np.ndarray = self.gen_empty_array()
        self._phantom_array: np.ndarray = self._gen_phantom_array()
        self.difficulty: str = difficulty
        self.show_process: bool = show_process
        self.delay: bool = delay
        self.delay_time: float = 0.1
        self._quadrant_size: int = self._calc_box_size()
        self.cur_row = 0
        self.cur_col = 0
        sys.setrecursionlimit(1000000)

    def gen_empty_array(self) -> np.ndarray:
        array: list = []
        row: list = []
        for i in range(0, self._size):
            row.append(0)
        for j in range(0, self._size):
            array.append(row)
        np_array: np.ndarray = np.array(array)
        return np_array

    def _gen_phantom_array(self) -> np.ndarray:
        array: list = []
        row: list = []
        for i in range(0, self._size):
            z_list: list = []
            for z in range(0, self._size):
                z_list.append(0)
            row.append(z_list)
        for j in range(0, self._size):
            array.append(row)
        np_array: np.ndarray = np.array(array)
        return np_array

    def _calc_box_size(self) -> int:
        box: int = int(self._size ** 0.5)
        return box

    def _quadrant_bounds(self) -> tuple[int, int, int, int]:
        quadrant: int = math.ceil((self.cur_row + 1) / self._quadrant_size)
        index_top: int = int(quadrant * self._quadrant_size)
        index_bot: int = int(index_top - self._quadrant_size)

        quadrant: int = math.ceil((self.cur_col + 1) / self._quadrant_size)
        index_left: int = int(quadrant * self._quadrant_size)
        index_right: int = int(index_left - self._quadrant_size)

        return index_top, index_bot, index_left, index_right

    def _gen_solution(self) -> None:
        if self.cur_col == 0 and self.cur_row == 0:
            if self.array[self.cur_row][self.cur_col] != 0:
                self._phantom_array[:, self.cur_row, self.cur_col] = [self._size + 1 for x in range(0, self._size)]
        if self.show_process:
            self.clear_print(self.array)
            if self.delay:
                time.sleep(self.delay_time)
        if not self._test_finish():
            possible_n: np.ndarray = self._gen_possible_numbers()
            self._update_array_with_choice(possible_n)

    def _test_rules(self, n: int) -> bool:
        row_test: bool = self._test_row(n)
        col_test: bool = self._test_col(n)
        quadrant_test: bool = self._test_quadrant(n)
        return row_test and col_test and quadrant_test

    def _test_row(self, n: int) -> bool:
        if n in self.array[self.cur_row]:
            return False
        else:
            return True

    def _test_col(self, n: int) -> bool:
        if n in self.array[:, self.cur_col:(self.cur_col + 1)]:
            return False
        else:
            return True

    def _test_quadrant(self, n: int) -> bool:
        quadrant: tuple[int, int, int, int] = self._quadrant_bounds()
        if n in self.array[quadrant[1]:quadrant[0], quadrant[3]:quadrant[2]]:
            return False
        else:
            return True

    def _go_back(self) -> None:
        cell: np.ndarray = self._phantom_array[:, self.cur_row, self.cur_col].copy()
        if (self._size + 1) not in cell:
            self.array[self.cur_row][self.cur_col]: int = 0
        self._step_back()
        cell: np.ndarray = self._phantom_array[:, self.cur_row, self.cur_col].copy()
        self._update_array_with_choice(cell)

    def _step_back(self) -> None:
        if self.cur_col == 0:
            self.cur_col: int = 8
            self.cur_row -= 1
        else:
            self.cur_col -= 1

    def _go_forward(self) -> None:
        self._step_forward()
        if self._test_in_bounds():
            if self.array[self.cur_row][self.cur_col] != 0:
                self._phantom_array[:, self.cur_row, self.cur_col] = [self._size + 1 for x in range(0, self._size)]
                if not self._test_finish():
                    self._go_forward()

    def _step_forward(self) -> None:
        if self.cur_col == 8:
            self.cur_col: int = 0
            self.cur_row += 1
        else:
            self.cur_col += 1

    def _test_finish(self) -> bool:
        if 0 not in self.array:
            return True
        else:
            return False

    def _test_in_bounds(self) -> bool:
        if self.cur_row >= self._size:
            return False
        else:
            return True

    def _gen_possible_numbers(self) -> np.ndarray:
        possible_n: list = []
        for n in range(1, self._size + 1):
            if self._test_rules(n):
                possible_n.append(n)
            else:
                possible_n.append(0)
        return np.array(possible_n)

    def _update_array_with_choice(self, possible_n: np.ndarray) -> None:
        if (self._size + 1) not in possible_n:
            if collections.Counter(possible_n)[0] == self._size:
                self._go_back()
            else:
                n_choice: int = random.choice([x for x in possible_n if x != 0])
                possible_n[possible_n == n_choice]: int = 0

                self.array[self.cur_row][self.cur_col]: int = n_choice
                self._populate_phantom_array(possible_n)
                if not self._test_finish():
                    self._go_forward()
                    self._gen_solution()
        else:
            self._go_back()

    def _populate_phantom_array(self, numbers: np.ndarray) -> None:
        self._phantom_array[:, self.cur_row, self.cur_col] = numbers

    # change to generate a puzzle with only one solution
    def _gen_riddle(self) -> None:
        choices: list = []
        if self.difficulty.lower() == "easy":
            sample = random.randint(int(self._quadrant_size * 4), int(self._quadrant_size * 5))
        elif self.difficulty.lower() == "normal":
            sample = random.randint(int(self._quadrant_size * 3), int(self._quadrant_size * 4))
        elif self.difficulty.lower() == "hard":
            sample = random.randint(int(self._quadrant_size * 2), int(self._quadrant_size * 3))
        else:
            sample = random.randint(int(self._quadrant_size * 4), int(self._quadrant_size * 5))

        while len(choices) != sample:
            row: int = random.randint(0, self._size - 1)
            col: int = random.randint(0, self._size - 1)

            if (row, col) not in choices:
                choices.append((row, col))

        for t in choices:
            self.riddle[t[0]][t[1]]: int = self.array[t[0]][t[1]]
        self.sudoku_print(self.riddle)

    def sudoku_print(self, array) -> None:
        print("\n")
        for i in range(0, len(array)):
            row: str = ""
            for j in range(0, len(array)):
                if (j + 1) % self._quadrant_size == 0:
                    if j + 1 != self._size:
                        row += f" {array[i][j]} "
                        row += "|"
                    else:
                        row += f" {array[i][j]} "
                else:
                    row += f" {array[i][j]} "
            print(row)
            if (i + 1) % self._quadrant_size == 0:
                if (i + 1) != self._size:
                    print("----------------------------")

    def clear_print(self, array) -> None:
        clear()
        self.sudoku_print(array)

    def _gen_possibility_array_start(self):
        self.go_to_start()
        self._gen_possibility_array()
        self.go_to_start()

    def _gen_possibility_array(self) -> None:
        possible_n = self._gen_possible_numbers()
        self._populate_phantom_array(possible_n)
        self._go_forward()
        if self._test_in_bounds():
            self._gen_possibility_array()

    def go_to_start(self):
        self.cur_row: int = 0
        self.cur_col: int = 0

    def _unambiguous_cells(self):
        self.go_to_start()
        self._gen_possibility_array()
        self.go_to_start()
        self._unambiguous_cells_row()
        self.go_to_start()
        self._unambiguous_cells_col()
        self.go_to_start()
        self._unambiguous_cells_quadrant()

#  works. build for col and quadrants
    def _unambiguous_cells_row(self):
        phantom_row: np.ndarray = self._phantom_array[:, self.cur_row, :]
        counter: int = 0
        unambiguous_values: list = []
        counts: tuple[np.ndarray, np.ndarray] = np.unique(phantom_row, return_counts=True)
        for n in counts[0]:
            n_count = counts[1][counter]
            if n_count == 1:
                unambiguous_values.append(n)
            counter += 1

        if len(unambiguous_values) > 0:
            for n in unambiguous_values:
                for cell in range(0, self._size):
                    possible_n = phantom_row[:, cell]
                    if n in possible_n:
                        self.cur_col = cell
                        self.array[self.cur_row, self.cur_col] = n
                        self._gen_possibility_array_start()
                        self._unambiguous_cells_row()
        if self.cur_row != 8:
            self.cur_row += 1
            self._unambiguous_cells_row()

    def _unambiguous_cells_col(self):
        phantom_col: np.ndarray = self._phantom_array[:, :, self.cur_col]
        counter: int = 0
        unambiguous_values: list = []
        counts: tuple[np.ndarray, np.ndarray] = np.unique(phantom_col, return_counts=True)
        for n in counts[0]:
            n_count = counts[1][counter]
            if n_count == 1:
                unambiguous_values.append(n)
            counter += 1

        if len(unambiguous_values) > 0:
            for n in unambiguous_values:
                for cell in range(0, self._size):
                    possible_n = phantom_col[:, cell]
                    if n in possible_n:
                        self.cur_row = cell
                        self.array[self.cur_row, self.cur_col] = n
                        self._gen_possibility_array_start()
                        self._unambiguous_cells_col()
        if self.cur_col != 8:
            self.cur_col += 1
            self._unambiguous_cells_col()

    def _unambiguous_cells_quadrant(self):
        bounds: tuple = self._quadrant_bounds()
        phantom_quadrant: np.ndarray = self._phantom_array[:, bounds[1]:bounds[0], bounds[3]:bounds[2]]
        counter: int = 0
        unambiguous_values: list = []
        counts: tuple[np.ndarray, np.ndarray] = np.unique(phantom_quadrant, return_counts=True)
        for n in counts[0]:
            n_count = counts[1][counter]
            if n_count == 1:
                unambiguous_values.append(n)
            counter += 1
        if len(unambiguous_values) > 0:
            for n in unambiguous_values:
                for row in range(0, self._quadrant_size):
                    for col in range(0, self._quadrant_size):
                        possible_n = phantom_quadrant[:, row, col]
                        if n in possible_n:
                            self.array[bounds[1]:bounds[0], bounds[3]:bounds[2]][row, col] = n
                            self._gen_possibility_array_start()
                            self._unambiguous_cells_quadrant()
        if self.cur_col != self._size - self._quadrant_size:
            self.cur_col += self._quadrant_size
            self._unambiguous_cells_quadrant()
        elif self.cur_row != self._size - self._quadrant_size:
            self.cur_row += self._quadrant_size
            self._unambiguous_cells_quadrant()

    def test(self, array):
        pass

    def solve(self, array: np.ndarray) -> None:
        start = time.time()
        self.array = array.copy()
        self.soft_solve(array)
        self.go_to_start()
        self._gen_phantom_array()
        self._gen_solution()
        self.clear_print(self.array)
        end = time.time() - start
        print(f"Duration: {end}")

    def gen_sudoku(self) -> np.ndarray:
        pass

    def soft_solve(self, array: np.ndarray) -> None:
        self.go_to_start()
        self.array = array.copy()
        self._gen_phantom_array()
        self._gen_possibility_array()
        self._unambiguous_cells()
        if self.show_process:
            self.clear_print(self.array)
        if not (array == self.array).all():
            self.soft_solve(self.array)
