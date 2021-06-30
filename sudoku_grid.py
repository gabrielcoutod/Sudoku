import random
from typing import Callable


class SudokuGrid:
    """
    Simulates a sudoku grid with the cells being numbered in the following way

    0       1       2       3       4       5       6       7       8
    9       10      11      12      13      14      15      16      17
    18      19      20      21      22      23      24      25      26
    27      28      29      30      31      32      33      34      35
    36      37      38      39      40      41      42      43      44
    45      46      47      48      49      50      51      52      53
    54      55      56      57      58      59      60      61      62
    63      64      65      66      67      68      69      70      71
    72      73      74      75      76      77      78      79      80

    """

    MAX_NUMBER = 9  # the highest number you can put in a cell and the number of cells in a line, column or subgrid
    GRID_SIZE = 81  # total number of cells in the grid
    sub_grids = {}  # dict that given a cell position returns the grid it is in
    INVALID_VALUE = -1  # the value that indicates a cell is empty
    ERROR = -1  # indicates a value for a given cell couldn't be found
    MAX_REMOVE = 35  # maximum number of removed numbers from grid

    def __init__(self):
        """
        Initializes the grid and the first time it is run initializes the sub_grids
        """
        self.grid = []  # the grid that will have missing pieces to complete
        self.sol = [SudokuGrid.INVALID_VALUE for i in range(SudokuGrid.GRID_SIZE)]  # the grid with the solution
        if not SudokuGrid.sub_grids:
            SudokuGrid.init_sub_grids()

    @staticmethod
    def init_sub_grids():
        """
        Initializes the dict that given a cell position returns the grid it is in
        """
        SudokuGrid.sub_grids.update(
            dict.fromkeys([0, 1, 2, 9, 10, 11, 18, 19, 20], [0, 1, 2, 9, 10, 11, 18, 19, 20]))
        SudokuGrid.sub_grids.update(
            dict.fromkeys([3, 4, 5, 12, 13, 14, 21, 22, 23], [3, 4, 5, 12, 13, 14, 21, 22, 23]))
        SudokuGrid.sub_grids.update(
            dict.fromkeys([6, 7, 8, 15, 16, 17, 24, 25, 26], [6, 7, 8, 15, 16, 17, 24, 25, 26]))
        SudokuGrid.sub_grids.update(
            dict.fromkeys([27, 28, 29, 36, 37, 38, 45, 46, 47], [27, 28, 29, 36, 37, 38, 45, 46, 47]))
        SudokuGrid.sub_grids.update(
            dict.fromkeys([30, 31, 32, 39, 40, 41, 48, 49, 50], [30, 31, 32, 39, 40, 41, 48, 49, 50]))
        SudokuGrid.sub_grids.update(
            dict.fromkeys([33, 34, 35, 42, 43, 44, 51, 52, 53], [33, 34, 35, 42, 43, 44, 51, 52, 53]))
        SudokuGrid.sub_grids.update(
            dict.fromkeys([54, 55, 56, 63, 64, 65, 72, 73, 74], [54, 55, 56, 63, 64, 65, 72, 73, 74]))
        SudokuGrid.sub_grids.update(
            dict.fromkeys([57, 58, 59, 66, 67, 68, 75, 76, 77], [57, 58, 59, 66, 67, 68, 75, 76, 77]))
        SudokuGrid.sub_grids.update(
            dict.fromkeys([60, 61, 62, 69, 70, 71, 78, 79, 80], [60, 61, 62, 69, 70, 71, 78, 79, 80]))

    def reset(self):
        """
        Makes the grids return to their initial state
        """
        self.sol = [SudokuGrid.INVALID_VALUE for i in range(SudokuGrid.GRID_SIZE)]
        self.grid = []

    @staticmethod
    def print_grid(grid: list):
        """
        Prints a grid
        """
        i = 0
        while i < SudokuGrid.GRID_SIZE:
            print(f"{grid[i]}\t", end="")
            i += 1
            if i % SudokuGrid.MAX_NUMBER == 0:
                print()

    def ok_value(self, grid: list, value: int, pos: int) -> bool:
        """
        Checks if putting a value in a cell of a given grid is ok
        """

        backup = grid[pos]  # backup of the previous value
        grid[pos] = SudokuGrid.INVALID_VALUE  # so it doesn't interfere with the test

        sub_grid = SudokuGrid.sub_grids[pos]  # gets a list with the elements of the sub_grid
        line = pos // SudokuGrid.MAX_NUMBER * SudokuGrid.MAX_NUMBER  # gets the index of the first element of the line
        col = pos % SudokuGrid.MAX_NUMBER  # gets the index of the first element of the column

        for i in range(SudokuGrid.MAX_NUMBER):
            if grid[line + i] == value or grid[col + SudokuGrid.MAX_NUMBER * i] == value or grid[sub_grid[i]] == value:
                grid[pos] = backup
                return False

        grid[pos] = backup
        return True

    def give_value(self, grid: list, pos: int, vals: list) -> int:
        """
        Returns and changes the given value in the pos of the grid for a valid value from vals.
        """
        number = vals.pop()  # so the value can't be used again
        while not self.ok_value(grid, number, pos):  # if the value isn't ok
            if not vals:  # if tried all the values returns ERROR
                return SudokuGrid.ERROR
            number = vals.pop()  # tries with another value

        grid[pos] = number  # if an ok value is found puts it in the grid
        return number

    def create(self):
        """
        Creates a sudoku grid
        """
        self.solution(self.sol, [i for i in range(SudokuGrid.GRID_SIZE)], SudokuGrid.GRID_SIZE - 1, random.shuffle)

    def solution(self, grid: list, list_pos: list, end: int = GRID_SIZE - 1,
                 foo: Callable[[list], any] = lambda arg: None, beg: int = 0) -> bool:
        """
        Recursively fills a sudoku section([list_pos[beg],list_pos[end]) from the grid
        foo alters the order of the possible variables for a cell
        """
        if beg == end + 1:  # if got past the region
            return True

        vals = list(range(1, SudokuGrid.MAX_NUMBER + 1))  # creates a list of valid values for cells
        foo(vals)  # possibly changes the order of the values

        number = self.give_value(grid, list_pos[beg], vals)  # tries to give a valid value to put in a cell
        if number == SudokuGrid.ERROR:  # if can't give a valid value
            return False

        while not self.solution(grid, list_pos, end, foo, beg + 1):  # recursevily tries to fill the section
            grid[list_pos[beg]] = SudokuGrid.INVALID_VALUE  # because the previous value was not ok
            if not vals:  # if the list of values is empty
                return False

            number = self.give_value(grid, list_pos[beg], vals)  # tries to give a valid value to put in a cell
            if number == SudokuGrid.ERROR:  # if can't give a valid value
                return False

        return True

    def remove_cells(self):
        """
        Removes cells from the sudoku solution
        """
        self.grid = self.sol[:]  # copies the solution
        pos = [i for i in range(SudokuGrid.GRID_SIZE)]  # creates a list with positions
        random.shuffle(pos)  # shuffles the list
        i = 0  # to iterate through pos
        removed = 0  # number of removed values

        while i < len(pos) and removed < SudokuGrid.MAX_REMOVE:
            backup = self.grid[pos[i]]  # makes a backup in case it gives two different solutions
            self.grid[pos[i]] = SudokuGrid.INVALID_VALUE  # removes i element in pos
            grid_1 = self.grid[:]
            grid_2 = self.grid[:]

            self.solution(grid_1, pos, i)
            self.solution(grid_2, pos, i, lambda x: x.reverse())
            if grid_1 != grid_2:  # if there are two solutions puts the value back in
                self.grid[pos[i]] = backup
            else:
                removed += 1
            i += 1


if __name__ == '__main__':
    val = SudokuGrid()
    val.create()  # creates the solution
    val.remove_cells()  # removes grids
    SudokuGrid.print_grid(val.grid)  # grid with numbers removed
    print()  # \n
    SudokuGrid.print_grid(val.sol)  # solution
