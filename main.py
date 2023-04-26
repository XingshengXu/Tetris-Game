import pygame
import random

pygame.font.init()

# Game constants
WIDTH, HEIGHT = 800, 700
SQUARE_SIZE = 30
ROWS, COLS = HEIGHT // SQUARE_SIZE, WIDTH // SQUARE_SIZE
BACKGROUND_COLOR = (30, 30, 30)
GRID_COLOR = (128, 128, 128)
TEXT_COLOR = (255, 255, 255)

# Tetromino shapes
SHAPES = [
    [
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [0, 1, 1],
        [1, 1, 0]
    ],
    [
        [1, 1, 0],
        [0, 1, 1]
    ],
    [
        [1, 1],
        [1, 1]
    ],
    [
        [1, 1, 1, 1]
    ],
    [
        [1, 1, 0],
        [0, 1, 1]
    ],
    [
        [0, 1, 1],
        [1, 1, 0]
    ]
]

# Colors
COLORS = [
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 0),
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 165, 0)
]


class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]

    def rotate(self):
        self.shape = list(zip(*reversed(self.shape)))


class Tetris:
    def __init__(self):
        self.grid = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]
        self.current_piece = self.get_new_piece()
        self.game_over = False

    def get_new_piece(self):
        shape = random.choice(SHAPES)
        x, y = COLS // 2 - len(shape[0]) // 2, 0
        return Tetromino(x, y, shape)

    def valid_position(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                try:
                    if cell and self.grid[y + piece.y][x + piece.x]:
                        return False
                except IndexError:
                    return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.current_piece.y][x +
                                                        self.current_piece.x] = self.current_piece.color
        self.current_piece = self.get_new_piece()

        if not self.valid_position(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for i, row in enumerate(self.grid):
            if all(cell != (0, 0, 0) for cell in row):
                lines_cleared += 1
                self.grid.pop(i)
                self.grid.insert(0, [(0, 0, 0) for _ in range(COLS)])
        return lines_cleared


def draw_grid(surface, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            pygame.draw.rect(surface, cell, (x * SQUARE_SIZE,
                             y * SQUARE_SIZE, SQUARE_SIZE - 1, SQUARE_SIZE - 1))


def draw_window(surface, grid):
    surface.fill(BACKGROUND_COLOR)

    for i in range(ROWS + 1):
        pygame.draw.line(surface, GRID_COLOR,
                         (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE))
    for i in range(COLS + 1):
        pygame.draw.line(surface, GRID_COLOR,
                         (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT))

    draw_grid(surface, grid)

    font = pygame.font.Font(None, 36)
    text = font.render("Press ESC to exit", True, TEXT_COLOR)
    surface.blit(text, (10, 10))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    tetris = Tetris()

    fall_time = 0
    fall_speed = 500
    pygame.time.set_timer(pygame.USEREVENT, fall_speed)

    while not tetris.game_over:
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.current_piece.x -= 1
                    if not tetris.valid_position(tetris.current_piece):
                        tetris.current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    tetris.current_piece.x += 1
                    if not tetris.valid_position(tetris.current_piece):
                        tetris.current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    tetris.current_piece.y += 1
                    if not tetris.valid_position(tetris.current_piece):
                        tetris.current_piece.y -= 1
                        tetris.lock_piece()
                        tetris.clear_lines()
                if event.key == pygame.K_UP:
                    tetris.current_piece.rotate()
                    if not tetris.valid_position(tetris.current_piece):
                        for _ in range(3):
                            tetris.current_piece.rotate()

            if event.type == pygame.USEREVENT:
                tetris.current_piece.y += 1
                if not tetris.valid_position(tetris.current_piece):
                    tetris.current_piece.y -= 1
                    tetris.lock_piece()
                    tetris.clear_lines()

        grid_with_current_piece = [row.copy() for row in tetris.grid]
        for y, row in enumerate(tetris.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_with_current_piece[y + tetris.current_piece.y][x +
                                                                        tetris.current_piece.x] = tetris.current_piece.color

        draw_window(screen, grid_with_current_piece)
        pygame.display.flip()


if __name__ == "__main__":
    main()
