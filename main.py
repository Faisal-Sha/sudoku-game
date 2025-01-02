import pygame
import sys

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
HIGHLIGHT_COLOR = (0, 255, 0)  # Green color to highlight the selected cell

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')

# Initialize the Sudoku grid (empty cells represented by 0)
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

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
                text = FONT.render(str(grid[row][col]), True, BLACK)
                screen.blit(text, (col * CELL_SIZE + CELL_SIZE // 3, row * CELL_SIZE + CELL_SIZE // 3))

def draw(selected_cell):
    screen.fill(WHITE)
    draw_grid()
    draw_numbers()

    # Highlight the selected cell
    if selected_cell:
        row, col = selected_cell
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 4)

    pygame.display.update()

def main():
    selected_cell = None
    clock = pygame.time.Clock()

    while True:
        draw(selected_cell)  # Pass selected_cell to draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // CELL_SIZE, y // CELL_SIZE
                selected_cell = (row, col)

            if event.type == pygame.KEYDOWN:
                if selected_cell:
                    row, col = selected_cell
                    if event.key == pygame.K_1:
                        grid[row][col] = 1
                    elif event.key == pygame.K_2:
                        grid[row][col] = 2
                    elif event.key == pygame.K_3:
                        grid[row][col] = 3
                    elif event.key == pygame.K_4:
                        grid[row][col] = 4
                    elif event.key == pygame.K_5:
                        grid[row][col] = 5
                    elif event.key == pygame.K_6:
                        grid[row][col] = 6
                    elif event.key == pygame.K_7:
                        grid[row][col] = 7
                    elif event.key == pygame.K_8:
                        grid[row][col] = 8
                    elif event.key == pygame.K_9:
                        grid[row][col] = 9
                    elif event.key == pygame.K_0:
                        grid[row][col] = 0  # Clear the cell
                        
        clock.tick(30)

if __name__ == "__main__":
    main()
