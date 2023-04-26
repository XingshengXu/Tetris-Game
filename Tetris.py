from random import choice, randint
from sys import exit
import pygame as pg
from settings import *

pg.init()


class Tetrimino(pg.sprite.Sprite):
    def __init__(self, tetriminosType):
        super().__init__()
        self.type = tetriminosType
        self.frame_counter = 0
        self.is_horizontal = True

        # Load Tetrimino Image
        self.image = pg.transform.scale(pg.image.load(
            TETRIMINOS[self.type]).convert(), TETRIMINO_DIMENSIONS[self.type])
        self.rect = self.image.get_rect(topleft=TETRIMINO_SPAWN_POS)

    def tetrimino_fall(self):
        if self.frame_counter % 15 == 0:
            self.rect.y += MOVING_SPEED

    def tetrimino_rotate(self):
        if self.type == 'I':
            if self.is_horizontal:
                self.rect.x += GRID_WIDTH
                self.rect.y -= GRID_WIDTH
                self.image = pg.transform.rotate(self.image, 90)
                self.is_horizontal = False
            else:
                # self.rect.x -= GRID_WIDTH
                # self.rect.y += GRID_WIDTH
                self.image = pg.transform.rotate(self.image, -90)
                self.is_horizontal = True
        elif self.type == 'S':
            self.rect.x += GRID_WIDTH
            self.rect.y -= GRID_WIDTH
        elif self.type == 'Z':
            self.rect.x += GRID_WIDTH
            self.rect.y -= GRID_WIDTH
        # self.image = pg.transform.rotate(self.image, 90)

    def tetrimino_move(self):
        if self.frame_counter % 3 == 0:
            key = pg.key.get_pressed()
            if key[pg.K_DOWN]:
                self.rect.y += MOVING_SPEED
            elif key[pg.K_LEFT] and self.rect.left - MOVING_SPEED >= 0:
                self.rect.x -= MOVING_SPEED
            elif key[pg.K_RIGHT] and self.rect.right + MOVING_SPEED <= WIDTH - HUD_WIDTH:
                self.rect.x += MOVING_SPEED
            elif key[pg.K_UP]:
                self.tetrimino_rotate()

    def tetrimino_locked(self):
        if self.rect.bottom + MOVING_SPEED > HEIGHT:
            pg.event.post(pg.event.Event(TETRIMINO_LOCKED))
            self.kill()

    def update(self):
        self.frame_counter += FRAME_INCREMENT
        self.tetrimino_locked()
        self.tetrimino_fall()
        self.tetrimino_move()


class Game:

    def __init__(self):
        self.setup()
        self.load_images()

    def setup(self):
        self.game_active = False
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Tetris')

    def load_resources(self):
        self.load_images()

    def load_images(self):
        pass

    def draw_grid(self):
        x, y = 0, 0
        for _ in range(ROW_NUMBER):
            y += GRID_WIDTH
            pg.draw.line(self.screen, 'white', (0, y), (WIDTH-HUD_WIDTH, y))
        for _ in range(COLUMN_NUMBER):
            x += GRID_WIDTH
            pg.draw.line(self.screen, 'white', (x, 0), (x, HEIGHT))

    def draw_background(self):
        self.screen.fill('black')

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == TETRIMINO_LOCKED:
                tetriminos.add(Tetrimino('I'))

    def main_loop(self):
        """This is the game main loop."""
        while True:
            self.clock.tick(FPS)

            # Handle Events
            self.handle_events()

            # Display Game Background
            self.draw_background()

            # Draw Sprites
            tetriminos.draw(self.screen)
            # Update Sprites
            tetriminos.update()
            # Draw Grid
            self.draw_grid()
            pg.display.update()


# Create Class Instances and Add Sprites
game = Game()

tetriminos = pg.sprite.Group()
tetriminos.add(Tetrimino('I'))  # choice(list(TETRIMINOS.keys()))

# Run Main Loop
game.main_loop()
