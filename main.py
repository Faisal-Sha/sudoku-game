import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 600, 650  # Increased height for the check button
GRID_SIZE = 9
CELL_SIZE = 600 // GRID_SIZE  # Keep grid size the same
LINE_WIDTH = 2
FONT = pygame.font.SysFont('Arial', 32)
BUTTON_FONT = pygame.font.SysFont('Arial', 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HIGHLIGHT_COLOR = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')

# Initialize the Sudoku grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
initial_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Global variables
selected_cell = None
message = ""
message_color = BLACK

def is_valid_move(grid, row, col, num):
    # Check row
    for i in range(GRID_SIZE):
        if i != col and grid[row][i] == num:
            return False
    
    # Check column
    for i in range(GRID_SIZE):
        if i != row and grid[i][col] == num:
            return False
    
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if (i != row or j != col) and grid[i][j] == num:
                return False
    
    return True

def check_solution():
    global message, message_color
    
    # Check if the grid is complete (no zeros)
    if any(0 in row for row in grid):
        message = "Incomplete solution!"
        message_color = RED
        return False
    
    # Check each cell's validity
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = grid[row][col]
            # Temporarily set cell to 0 to check if the number is valid in its position
            grid[row][col] = 0
            if not is_valid_move(grid, row, col, num):
                grid[row][col] = num  # Restore the number
                message = "Incorrect solution!"
                message_color = RED
                return False
            grid[row][col] = num  # Restore the number
    
    message = "Congratulations! Solution is correct!"
    message_color = GREEN
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
    all_positions = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE)]
    random.shuffle(all_positions)
    
    for i in range(num_cells_to_remove):
        row, col = all_positions[i]
        grid[row][col] = 0

def draw_grid():
    for i in range(GRID_SIZE + 1):
        thickness = LINE_WIDTH if i % 3 != 0 else 4
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (600, i * CELL_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, 600), thickness)

def draw_numbers():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != 0:
                color = BLACK if initial_grid[row][col] != 0 else BLUE
                text = FONT.render(str(grid[row][col]), True, color)
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2,
                                                row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

def draw_selected_cell():
    if selected_cell:
        row, col = selected_cell
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 5)

def draw_check_button():
    button_rect = pygame.Rect(200, 610, 200, 30)
    pygame.draw.rect(screen, GRAY, button_rect)
    text = BUTTON_FONT.render("Check Solution", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

def draw_message():
    if message:
        text = BUTTON_FONT.render(message, True, message_color)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 15))
        screen.blit(text, text_rect)

def draw():
    screen.fill(WHITE)
    draw_grid()
    draw_numbers()
    draw_selected_cell()
    button_rect = draw_check_button()
    draw_message()
    pygame.display.update()
    return button_rect

def main():
    global grid, initial_grid, selected_cell, message, message_color
    clock = pygame.time.Clock()

    # Generate puzzle
    grid = generate_solved_grid()
    initial_grid = [row[:] for row in grid]
    remove_cells(grid, 40)
    initial_grid = [row[:] for row in grid]

    running = True
    while running:
        button_rect = draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < 600:  # Click in the grid
                    col, row = x // CELL_SIZE, y // CELL_SIZE
                    selected_cell = (row, col)
                elif button_rect.collidepoint(event.pos):  # Click on check button
                    check_solution()

            if event.type == pygame.KEYDOWN and selected_cell:
                row, col = selected_cell
                if initial_grid[row][col] == 0:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                   pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0,
                                   pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5,
                                   pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_KP0]:
                        if event.key in [pygame.K_0, pygame.K_KP0]:
                            num = 0
                        else:
                            num = event.key - pygame.K_0 if event.key <= pygame.K_9 else event.key - pygame.K_KP0
                        grid[row][col] = num
                        message = ""  # Clear any existing messages when the user makes a move

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()