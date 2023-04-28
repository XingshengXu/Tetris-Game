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

    def block_move(self):
        self.rect.topleft = self.coord * GRID_WIDTH

    def block_rotate(self, origin_coord):
        translated_coord = self.coord - origin_coord
        rotated_coord = translated_coord.rotate(90)
        return rotated_coord + origin_coord

    def check_collision(self, coord):
        x, y = int(coord.x), int(coord.y)
        if 0 <= x < FIELD_WIDTH and y < FIELD_HEIGHT and (y < 0 or not game.field_array[y][x]):
            return False
        return True

    def update(self):
        self.block_move()


class Tetromino():
    def __init__(self):
        self.type = choice(list(TETROMINOES.keys()))
        self.landing = False
        self.speed_up = False

        # Load Block Image
        block_img = load_sprite_sheet(
            TETROMINO_TILES, TILE_WIDTH, TILE_HEIGHT,
            customScale=True, size=(GRID_WIDTH, GRID_WIDTH))
        self.image = block_img[TETROMINO_TILETYPE[self.type]]
        self.blocks = [Block(self, coord) for coord in TETROMINOES[self.type]]

    def tetromino_rotate(self):
        origin_coord = self.blocks[0].coord
        new_block_coord = [block.block_rotate(
            origin_coord) for block in self.blocks]
        is_collide = self.is_collide(new_block_coord)
        if not is_collide:
            for block, new_coord in zip(self.blocks, new_block_coord):
                block.coord = new_coord

    def tetromino_fall(self):
        new_block_coord = [block.coord + MOVEMENTS['down']
                           for block in self.blocks]
        is_collide = self.is_collide(new_block_coord)

        if not is_collide:
            for block in self.blocks:
                block.coord += MOVEMENTS['down']
        else:
            self.landing = True

    def tetromino_move(self, direction=None):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            direction = 'left'
        elif key[pg.K_RIGHT]:
            direction = 'right'
        elif key[pg.K_UP]:
            self.tetromino_rotate()
        elif key[pg.K_DOWN]:
            self.speed_up = True
        if direction:
            new_block_coord = [block.coord + MOVEMENTS[direction]
                               for block in self.blocks]
            is_collide = self.is_collide(new_block_coord)

            if not is_collide:
                for block in self.blocks:
                    block.coord += MOVEMENTS[direction]

    def is_collide(self, block_coords):
        return any(Block.check_collision(block, coord) for block, coord in zip(self.blocks, block_coords))

    def put_tetromino_blocks_in_array(self):
        for block in self.blocks:
            x, y = int(block.coord.x), int(block.coord.y)
            game.field_array[y][x] = block

    def update(self):
        trigger = [game.fall_trigger, game.fast_fall_trigger][self.speed_up]
        if trigger:
            self.tetromino_fall()
        if game.anim_trigger:
            self.tetromino_move()
        if self.landing:
            self.speed_up = False
            self.put_tetromino_blocks_in_array()
            pg.time.delay(300)
            game.current_tetromino = game.spawn_tetromino()


class Game:

    def __init__(self):
        self.setup()
        self.load_images()
        self.field_array = self.get_field_array()
        self.tetrominos = pg.sprite.Group()
        self.current_tetromino = self.spawn_tetromino()

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

    def get_field_array(self):
        return [[0 for x in range(FIELD_WIDTH)] for y in range(FIELD_HEIGHT)]

    def set_timer(self):
        self.fall_trigger = False
        self.anim_trigger = False
        self.fast_fall_trigger = False
        pg.time.set_timer(FALL_TRIGGER, FALL_FREQ)
        pg.time.set_timer(ANIM_TRIGGER, ANIM_TRIGGER_FREQ)
        pg.time.set_timer(FAST_FALL_TRIGGER, FAST_FALL_FREQ)

    def spawn_tetromino(self):
        new_tetromino = Tetromino()
        self.tetrominos.add(new_tetromino.blocks)
        return new_tetromino

    def handle_events(self):
        self.fall_trigger = False
        self.anim_trigger = False
        self.fast_fall_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == FALL_TRIGGER:
                self.fall_trigger = True
            if event.type == ANIM_TRIGGER:
                self.anim_trigger = True
            if event.type == FAST_FALL_TRIGGER:
                self.fast_fall_trigger = True

    def main_loop(self):
        """This is the game main loop."""
        while True:
            self.clock.tick(FPS)

            # Handle Events
            self.handle_events()

            # Display Game Background
            self.draw_background()

            # Update Tetromino
            self.current_tetromino.update()

            # Draw Sprites
            self.tetrominos.draw(self.screen)
            # Update Sprites
            self.tetrominos.update()

            # Draw Grid
            self.draw_grid()

            pg.display.update()


# Create Class Instances and Sprite Group
game = Game()

# Run Main Loop
game.main_loop()
