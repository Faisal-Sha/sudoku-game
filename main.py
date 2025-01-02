import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 2
FONT = pygame.font.SysFont('Arial', 32)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HIGHLIGHT_COLOR = (255, 255, 0)  # Yellow highlight for selected cell
BLUE = (0, 0, 255)  # For user-entered numbers

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')

# Initialize the Sudoku grid (empty cells represented by 0)
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
initial_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # For storing initial values

# Global selected cell
selected_cell = None

def is_valid_move(grid, row, col, num):
    # Check the row
    for i in range(GRID_SIZE):
        if grid[row][i] == num:
            return False
    # Check the column
    for i in range(GRID_SIZE):
        if grid[i][col] == num:
            return False
    # Check the 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True

def solve(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(grid, row, col, num):
                        grid[row][col] = num
                        if solve(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def generate_solved_grid():
    grid_copy = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    solve(grid_copy)
    return grid_copy

def remove_cells(grid, num_cells_to_remove):
    # Create a list of all positions in the grid
    all_positions = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE)]
    random.shuffle(all_positions)
    
    # Remove random cells
    for i in range(num_cells_to_remove):
        row, col = all_positions[i]
        grid[row][col] = 0  # Remove the value by setting it to 0

def draw_grid():
    # Draw the grid
    for i in range(GRID_SIZE + 1):
        thickness = LINE_WIDTH if i % 3 != 0 else 4  # Thicker lines for 3x3 box boundaries
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), thickness)

def draw_numbers():
    # Draw the numbers in the cells
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != 0:
                # Choose color based on whether the number was initial or user-entered
                color = BLACK if initial_grid[row][col] != 0 else BLUE
                text = FONT.render(str(grid[row][col]), True, color)
                # Center the text in the cell
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2,
                                                row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

def draw_selected_cell():
    if selected_cell:
        row, col = selected_cell
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 5)

def draw():
    screen.fill(WHITE)
    draw_grid()
    draw_numbers()
    draw_selected_cell()
    pygame.display.update()

def main():
    global grid, initial_grid, selected_cell
    clock = pygame.time.Clock()

    # Generate a solved grid and create a puzzle by removing cells
    grid = generate_solved_grid()
    initial_grid = [row[:] for row in grid]  # Save initial grid values
    remove_cells(grid, 40)  # Remove 40 cells to create a puzzle
    # Update initial_grid to match the puzzle state
    initial_grid = [row[:] for row in grid]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Update selected cell based on mouse click
                x, y = event.pos
                col, row = x // CELL_SIZE, y // CELL_SIZE
                selected_cell = (row, col)

            if event.type == pygame.KEYDOWN and selected_cell:
                row, col = selected_cell
                # Only allow editing on empty cells
                if initial_grid[row][col] == 0:  # If it's 0, it's an editable cell
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                   pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0,
                                   pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5,
                                   pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_KP0]:
                        # Convert keypress to number
                        if event.key in [pygame.K_0, pygame.K_KP0]:
                            num = 0
                        else:
                            num = event.key - pygame.K_0 if event.key <= pygame.K_9 else event.key - pygame.K_KP0
                        grid[row][col] = num

        draw()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()