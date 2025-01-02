import unittest

# The grid is represented as a 2D list (9x9 grid)
def is_valid_solution(grid):
    # Check each row
    for row in grid:
        if sorted(row) != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return False
    
    # Check each column
    for col in range(9):
        column = [grid[row][col] for row in range(9)]
        if sorted(column) != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return False
    
    # Check each 3x3 subgrid
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = []
            for i in range(3):
                for j in range(3):
                    box.append(grid[box_row + i][box_col + j])
            if sorted(box) != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                return False

    return True

# Unit tests for the validation function
class TestSudokuValidation(unittest.TestCase):

    def test_valid_solution(self):
        valid_grid = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        self.assertTrue(is_valid_solution(valid_grid))
    
    def test_invalid_row(self):
        invalid_row_grid = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 8]  # Invalid row (duplicate 8)
        ]
        self.assertFalse(is_valid_solution(invalid_row_grid))
    
    def test_invalid_column(self):
        invalid_column_grid = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        invalid_column_grid = invalid_column_grid.copy()
        invalid_column_grid[0][0] = 1  # Change value in column 0, row 0
        self.assertFalse(is_valid_solution(invalid_column_grid))

    def test_invalid_subgrid(self):
        invalid_subgrid_grid = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        invalid_subgrid_grid = invalid_subgrid_grid.copy()
        invalid_subgrid_grid[0][0] = 9  # Modify value in 3x3 subgrid
        self.assertFalse(is_valid_solution(invalid_subgrid_grid))


def is_valid(grid, row, col, num):
    # Check if 'num' is not in the given row
    for c in range(9):
        if grid[row][c] == num:
            return False
    
    # Check if 'num' is not in the given column
    for r in range(9):
        if grid[r][col] == num:
            return False
    
    # Check if 'num' is not in the 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if grid[r][c] == num:
                return False

    return True


def solve_sudoku(grid):
    # Find the first empty cell (represented by 0)
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                # Try each number from 1 to 9
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        # Place the number and try to solve the rest
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        # If it didn't work, backtrack
                        grid[row][col] = 0
                return False  # If no number is valid, return False
    return True  # If no empty cells remain, the puzzle is solved




# Unit tests for the Sudoku solver
class TestSudokuSolver(unittest.TestCase):

    def test_valid_sudoku_solution(self):
        grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        expected_solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        
        solve_sudoku(grid)
        self.assertEqual(grid, expected_solution)

    def test_unsolvable_sudoku(self):
        grid = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        grid[0][0] = 6  # Invalid modification (duplicate value)
        self.assertFalse(solve_sudoku(grid))  # This grid is unsolvable



if __name__ == '__main__':
    unittest.main()