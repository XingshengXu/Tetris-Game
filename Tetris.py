from random import choice, randint
from sys import exit
import pygame as pg
from settings import *

pg.init()


def load_sprite_sheet(sheet_path, sprite_width, sprite_height, needScale2x=False, customScale=False, size=None):
    """Splits a sprite sheet into multiple sub-sprites based on the given width and height, 
    and optionally scales them."""
    image = pg.image.load(sheet_path).convert()
    image_num = image.get_width() // sprite_width

    sprites = []
    for i in range(image_num):
        surface = pg.Surface((sprite_width, sprite_height))
        rect = pg.Rect(i * sprite_width, 0, sprite_width, sprite_height)
        surface.blit(image, (0, 0), rect)
        if needScale2x:
            surface = pg.transform.scale2x(surface)
        elif customScale:
            surface = pg.transform.scale(surface, size)
        sprites.append(surface)
    return sprites


class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, coord):
        super().__init__()
        self.tetromino = tetromino
        self.coord = vec(coord) + TETROMINO_SPAWN_OFFSET
        self.image = self.tetromino.image
        self.rect = self.image.get_rect(topleft=self.coord * GRID_WIDTH)
        self.dir = 'down'

    def tetromino_fall(self):
        new_coord = self.coord + MOVEMENTS['down']
        if not self.check_collision(new_coord):
            self.coord = new_coord
            self.rect.topleft = self.coord * GRID_WIDTH

    def tetromino_move(self):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.dir = 'left'
        elif key[pg.K_RIGHT]:
            self.dir = 'right'

        new_coord = self.coord + MOVEMENTS[self.dir]
        if not tetrominos.sprites.check_collision(new_coord):
            self.coord = new_coord
            self.rect.topleft = self.coord * GRID_WIDTH

    def check_collision(self, new_coord):
        x, y = int(new_coord.x), int(new_coord.y)
        if 0 <= x < FIELD_WIDTH and y < FIELD_HEIGHT:
            return False
        return True

    def update(self):
        if game.anim_trigger:
            self.tetromino_fall()
        if game.control_trigger:
            self.tetromino_move()


class Tetromino():
    def __init__(self, tetrominosType):
        self.type = tetrominosType

        # Load Block Image
        block_img = load_sprite_sheet(
            TETROMINO_TILES, TILE_WIDTH, TILE_HEIGHT,
            customScale=True, size=(GRID_WIDTH, GRID_WIDTH))
        self.image = block_img[TETROMINO_TILETYPE[self.type]]
        self.blocks = [Block(self, coord) for coord in TETROMINOES[self.type]]

    def is_collide(self, block_pos):
        return any(map(Block.is_collide, self.blocks, block_pos))
#     def Tetromino_locked(self):
#         if self.rect.bottom + MOVING_SPEED > HEIGHT:
#             pg.event.post(pg.event.Event(Tetromino_LOCKED))
#             self.kill()


class Game:

    def __init__(self):
        self.setup()
        self.load_images()

    def setup(self):
        self.game_active = False
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        pg.display.set_caption('Tetris')
        self.set_timer()

    def load_resources(self):
        self.load_images()

    def load_images(self):
        pass

    def draw_grid(self):
        x, y = 0, 0
        for _ in range(ROW_NUMBER + 1):
            pg.draw.line(self.screen, 'white', (0, y), (WIDTH-HUD_WIDTH, y), 1)
            y += GRID_WIDTH
        for _ in range(COLUMN_NUMBER + 1):
            pg.draw.line(self.screen, 'white', (x, 0), (x, HEIGHT), 1)
            x += GRID_WIDTH

    def draw_background(self):
        self.screen.fill('black')

    def set_timer(self):
        self.anim_trigger = False
        self.control_trigger = False
        pg.time.set_timer(FALL_TRIGGER, FALL_FREQ)
        pg.time.set_timer(CONTROL_TRIGGER, CONTROL_FREQ)

    def handle_events(self):
        self.anim_trigger = False
        self.control_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == FALL_TRIGGER:
                self.anim_trigger = True
            if event.type == CONTROL_TRIGGER:
                self.control_trigger = True
            # if event.type == Tetromino_LOCKED:
            #     Tetrominos.add(Tetromino('I'))

    def main_loop(self):
        """This is the game main loop."""
        while True:
            self.clock.tick(FPS)

            # Handle Events
            self.handle_events()

            # Display Game Background
            self.draw_background()

            # Draw Sprites
            tetrominos.draw(self.screen)
            # Update Sprites
            tetrominos.update()

            # Draw Grid
            self.draw_grid()

            pg.display.update()


# Create Class Instances and Add Sprites
game = Game()

tetrominos = pg.sprite.SingleGroup()
tetrominos.add(Tetromino('Z').blocks)

# Run Main Loop
game.main_loop()
