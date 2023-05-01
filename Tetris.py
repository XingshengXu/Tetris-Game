from random import choice, uniform, randrange
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


def render_font(text, font, color, center):
    """Renders a given text using the specified font and color."""
    rendered_text = font.render(text, True, color)
    rendered_text_rect = rendered_text.get_rect(center=center)
    return rendered_text, rendered_text_rect


class Block(pg.sprite.Sprite):
    """Represents an individual block of a Tetromino."""

    def __init__(self, tetromino, coord):
        super().__init__()
        self.tetromino = tetromino
        self.coord = vec(coord) + TETROMINO_SPAWN_OFFSET
        self.image = self.tetromino.image
        self.rect = self.image.get_rect(topleft=self.coord * GRID_WIDTH)
        self.alive = True

        # Special Effects
        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(200)
        self.sfx_speed = uniform(0.2, 0.6)
        self.sfx_cycles = randrange(6, 8)
        self.cycle_counter = 0

    def sfx_duration(self):
        if game.anim_trigger and self.cycle_counter < self.sfx_cycles:
            self.cycle_counter += 1
        return self.cycle_counter >= self.sfx_cycles

    def sfx_play(self):
        self.image = self.sfx_image
        self.coord.y -= self.sfx_speed
        self.image = pg.transform.rotate(
            self.image, pg.time.get_ticks() * self.sfx_speed)

    def block_move(self):
        self.rect.topleft = self.coord * GRID_WIDTH

    def block_rotate(self, origin_coord, rotation_idx):
        translated_coord = self.coord - origin_coord
        rotation_idx_curr = (
            rotation_idx - 1) % len(TETROMINO_ROTATIONS[self.tetromino.type])
        translated_idx = TETROMINO_ROTATIONS[self.tetromino.type][rotation_idx_curr].index(
            translated_coord)
        rotated_coord = TETROMINO_ROTATIONS[self.tetromino.type][rotation_idx][translated_idx]
        return vec(rotated_coord) + origin_coord

    def block_destory(self):
        if not self.alive:
            if not self.sfx_duration():
                self.sfx_play()
            else:
                self.kill()

    def check_collision(self, coord):
        x, y = int(coord.x), int(coord.y)
        if 0 <= x < FIELD_WIDTH and y < FIELD_HEIGHT and (y < 0 or not game.field_array[y][x]):
            return False
        return True

    def update(self):
        self.block_destory()
        self.block_move()


class Tetromino():
    """Represents a Tetromino object made up of individual blocks."""

    def __init__(self):
        self.type = choice(list(TETROMINOES.keys()))
        self.rotation_idx = 0
        self.landing = False
        self.speed_up = False

        # Load Block Image
        block_img = load_sprite_sheet(
            TETROMINO_TILES, TILE_WIDTH, TILE_HEIGHT,
            customScale=True, size=(GRID_WIDTH, GRID_WIDTH))
        self.image = block_img[TETROMINO_TILETYPE[self.type]]
        self.blocks = [Block(self, coord) for coord in TETROMINOES[self.type]]

    def tetromino_rotate(self):
        self.rotation_idx = (self.rotation_idx +
                             1) % len(TETROMINO_ROTATIONS[self.type])
        origin_coord = self.blocks[0].coord
        new_block_coord = [block.block_rotate(
            origin_coord, self.rotation_idx) for block in self.blocks]
        is_collide = self.is_collide(new_block_coord)
        if not is_collide:
            for block, new_coord in zip(self.blocks, new_block_coord):
                block.coord = new_coord
        else:
            self.rotation_idx = (self.rotation_idx -
                                 1) % len(TETROMINO_ROTATIONS[self.type])

    def tetromino_fall(self):
        new_block_coord = [block.coord + MOVEMENTS['down']
                           for block in self.blocks]
        is_collide = self.is_collide(new_block_coord)

        if not is_collide:
            for block in self.blocks:
                block.coord += MOVEMENTS['down']
        else:
            self.landing = True
        self.speed_up = False

    def tetromino_move(self, direction=None):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            direction = 'left'
        elif key[pg.K_RIGHT]:
            direction = 'right'
        elif key[pg.K_UP]:
            self.tetromino_rotate()
            game.rotate_sound.play()
            game.rotate_sound.set_volume(0.3)
        elif key[pg.K_DOWN]:
            self.speed_up = True
            game.fall_sound.play()
            game.fall_sound.set_volume(0.3)

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
            if game.is_game_over():
                game.game_active = False
                game.play_gameover_music()
                pg.time.delay(GAMEOVER_DELAY)
            else:
                game.landing_sound.play()
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                game.current_tetromino = game.spawn_tetromino()


class Game:
    """Main game class for Tetris Game.
    The Game class is the core component of the Tetris game, managing the main game loop, 
    game events, and rendering. It is responsible for handling user input, updating the 
    game state, and drawing the game objects on the screen."""

    def __init__(self):
        self.setup()
        self.load_resources()

    def setup(self):
        self.game_active = False
        self.score = 0
        self.level = 0
        self.full_lines = 0
        self.total_lines = 0
        self.frame_counter = 0
        self.field_array = self.get_field_array()
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        pg.display.set_caption('Tetris')
        self.tetrominos = pg.sprite.Group()
        self.next_tetromino = self.generate_tetromino()
        self.current_tetromino = self.spawn_tetromino()
        self.clock = pg.time.Clock()
        self.set_timer()

    def load_resources(self):
        self.load_fonts()
        self.load_images()
        self.load_sounds()

    def load_fonts(self):
        self.next_text, self.next_text_rect = render_font(
            'Next', GAME_FONT, 'white', NEXT_TEXT_POS)
        self.score_text, self.score_text_rect = render_font(
            'Score', GAME_FONT, 'white', SCORE_TEXT_POS)
        self.level_text, self.level_text_rect = render_font(
            'Level', GAME_FONT, 'white', LEVEL_TEXT_POS)
        self.game_mainName, self.game_mainName_rect = render_font(
            'Tetris', TITLE_FONT, 'yellow2', (WIDTH // 2, GAMENAME_HEIGHT))
        self.game_message, self.game_message_rect = render_font(
            'Press Space to Play', GAME_FONT, 'green', (WIDTH // 2, GAMEMESSAGE_HEIGHT))
        self.score_HUD, self.score_HUD_rect = render_font(
            'Your Final Score:', GAME_FONT, 'green', (WIDTH // 2, GAMEMESSAGE_HEIGHT))

    def load_images(self):
        self.background_img = pg.transform.scale(
            pg.image.load(BACKGROUND_IMAGE).convert(), (WIDTH, HEIGHT))
        self.manualHUD_img = pg.transform.scale(
            pg.image.load(MANUAL_HUD).convert_alpha(), (400, 300))

    def load_sounds(self):
        self.play_pregame_music()
        self.line_clear_sound = pg.mixer.Sound(LINE_CLEAR_SOUND)
        self.four_line_clear_sound = pg.mixer.Sound(FOURLINE_CLEAR_SOUND)
        self.rotate_sound = pg.mixer.Sound(ROTATE_SOUND)
        self.fall_sound = pg.mixer.Sound(FALL_SOUND)
        self.levelup_sound = pg.mixer.Sound(LEVELUP_SOUND)
        self.landing_sound = pg.mixer.Sound(LANDING_SOUND)

    def play_pregame_music(self):
        pg.mixer.music.load(PREGAME_MUSIC)
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.5)

    def play_gameover_music(self):
        pg.mixer.music.load(GAMEOVER_MUSIC)
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play()
        pg.mixer.music.set_endevent(NEXT_MUSIC)

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
        self.draw_next_tetromino()
        self.display_HUD()

    def get_field_array(self):
        return [[0 for x in range(FIELD_WIDTH)] for y in range(FIELD_HEIGHT)]

    def check_full_lines(self):
        # Start at the bottom row of the field
        row = FIELD_HEIGHT - 1
        # Iterate through each row from bottom to top
        for y in range(FIELD_HEIGHT - 1, -1, -1):
            # Iterate through each cell in the row
            for x in range(FIELD_WIDTH):
                # Copy the cell from row y to row 'row'
                self.field_array[row][x] = self.field_array[y][x]
                # Update the coordinates of the cell if it exists
                if self.field_array[y][x]:
                    self.field_array[row][x].coord = vec(x, y)
            # Check if the row is not full
            if sum([bool(cell) for cell in self.field_array[y]]) < FIELD_WIDTH:
                row -= 1
            else:
                # The row is full, so mark each cell as not alive and set its value to 0
                for x in range(FIELD_WIDTH):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                # Increment the count of full lines
                self.full_lines += 1

    def update_fall_speed(self):
        levup_fall_freq = max(FAST_FALL_FREQ, FALL_FREQ -
                              self.level * LEVELUP_FREQ)
        pg.time.set_timer(FALL_TRIGGER, levup_fall_freq)

    def cal_score(self):
        if self.full_lines == 4:
            self.four_line_clear_sound.play()
            self.four_line_clear_sound.set_volume(0.5)
        elif self.full_lines >= 1:
            self.line_clear_sound.play()
            self.line_clear_sound.set_volume(0.5)

        self.score += REWARD_POINTS[self.full_lines] * (self.level + 1)
        self.total_lines += self.full_lines
        self.full_lines = 0

    def cal_level(self):
        previous_level = self.level
        self.level = self.total_lines // LEVELUP_LINES
        if previous_level != self.level:
            self.levelup_sound.play()
            self.levelup_sound.set_volume(0.5)
            self.update_fall_speed()

    def is_game_over(self):
        if self.current_tetromino.blocks[0].coord.y == TETROMINO_SPAWN_OFFSET[1]:
            return True

    def set_timer(self):
        self.fall_trigger = False
        self.anim_trigger = False
        self.fast_fall_trigger = False
        pg.time.set_timer(FALL_TRIGGER, FALL_FREQ)
        pg.time.set_timer(ANIM_TRIGGER, ANIM_TRIGGER_FREQ)
        pg.time.set_timer(FAST_FALL_TRIGGER, FAST_FALL_FREQ)

    def generate_tetromino(self):
        return Tetromino()

    def spawn_tetromino(self):
        new_tetromino = self.next_tetromino
        self.next_tetromino = self.generate_tetromino()
        self.tetrominos.add(new_tetromino.blocks)
        return new_tetromino

    def draw_next_tetromino(self):
        for block in self.next_tetromino.blocks:
            block_rect = block.image.get_rect(
                topleft=(block.coord * GRID_WIDTH) + NEXT_TETROMINO_OFFSET)
            self.screen.blit(block.image, block_rect)

    def display_HUD(self):
        self.screen.blit(self.next_text, self.next_text_rect)
        self.screen.blit(self.score_text, self.score_text_rect)
        self.screen.blit(self.level_text, self.level_text_rect)
        self.display_score()
        self.display_level()

    def display_score(self):
        """Display the score on the screen."""
        score, score_rect = render_font(
            f'{self.score}', GAME_FONT, 'white', SCORE_POS)
        self.screen.blit(score, score_rect)

    def display_level(self):
        """Display the level on the screen."""
        level, level_rect = render_font(
            f'{self.level}', GAME_FONT, 'white', LEVEL_POS)
        self.screen.blit(level, level_rect)

    def display_pregame_messages(self):
        # Display Game Main Title
        self.screen.blit(self.game_mainName, self.game_mainName_rect)
        self.screen.blit(self.manualHUD_img, MANUAL_HUD_POS)
        # Display Game Start Message
        if self.score == 0:
            if self.frame_counter % FPS < 30:
                self.screen.blit(self.game_message, self.game_message_rect)
        # Display Final Score
        else:
            self.screen.blit(self.score_HUD, self.score_HUD_rect)
            score_message, score_message_rect = render_font(
                f"{self.score}", GAME_FONT, 'green',
                (WIDTH // 2, SCOREMESSAGE_HEIGHT))
            self.screen.blit(score_message, score_message_rect)

    def reset_game(self):
        self.game_active = True
        self.score = 0
        self.level = 0
        self.full_lines = 0
        self.total_lines = 0
        self.frame_counter = 0
        self.field_array = self.get_field_array()
        self.tetrominos.empty()
        self.next_tetromino = self.generate_tetromino()
        self.current_tetromino = self.spawn_tetromino()
        self.set_timer()
        pg.mixer.music.stop()

    def handle_events(self):
        self.fall_trigger = False
        self.anim_trigger = False
        self.fast_fall_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if self.game_active:
                if event.type == FALL_TRIGGER:
                    self.fall_trigger = True
                if event.type == ANIM_TRIGGER:
                    self.anim_trigger = True
                if event.type == FAST_FALL_TRIGGER:
                    self.fast_fall_trigger = True
            else:
                if event.type == NEXT_MUSIC:
                    self.play_pregame_music()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.reset_game()

    def game_update(self):
        # Display Game Background
        self.draw_background()
        # Update Tetromino
        self.current_tetromino.update()
        # Draw Block Sprites
        self.tetrominos.draw(self.screen)
        # Update Block Sprites
        self.tetrominos.update()
        # Draw Grid
        self.draw_grid()
        # Check Full Lines
        self.check_full_lines()
        # Calculate Score
        self.cal_score()
        # Calculate Level
        self.cal_level()

    def main_loop(self):
        """This is the game main loop."""
        while True:
            self.clock.tick(FPS)
            self.frame_counter += 1
            self.handle_events()
            # Generate In-game Updates
            if self.game_active:
                self.game_update()
            else:
                # Generate Pre-game Screen
                self.screen.blit(self.background_img, (0, 0))
                self.display_pregame_messages()
            pg.display.update()


# Create Class Instances and Sprite Group
game = Game()

# Run Main Loop
game.main_loop()
