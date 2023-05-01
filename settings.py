import pygame as pg
pg.init()

"""
The settings module for the "Tetris" game. This module contains all the default settings for the gameplay. 
These settings can be easily accessed and used throughout the game by importing the module into the main game file.
"""

# Define a reference to the Vector2 class
vec = pg.math.Vector2

# Game Play Settings
FPS = 60
LEVELUP_LINES = 10
LEVELUP_FREQ = 20

MOVEMENTS = {
    'left': vec(-1, 0),
    'right': vec(1, 0),
    'down': vec(0, 1),
    'fastdown': vec(0, 1)
}

REWARD_POINTS = {
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}

# Game Dimensions
GRID_WIDTH = 40  # Grid Width
# HUD Dimensions
HUD_SIZE = HUD_WIDTH, HUD_HEIGHT = GRID_WIDTH * 5, GRID_WIDTH * 20
# Window Display Dimensions
SCREEN_SIZE = WIDTH, HEIGHT = GRID_WIDTH * 15, GRID_WIDTH * 20
# Game Coordinate Field Dimensions
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 10, 20
ROW_NUMBER = HEIGHT // GRID_WIDTH  # Row Number
COLUMN_NUMBER = (WIDTH - HUD_WIDTH) // GRID_WIDTH  # Column Number
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = 8, 8  # Tetromino Tile Dimensions
# Tetromino Spawn Position Offset
TETROMINO_SPAWN_OFFSET = vec(FIELD_WIDTH // 2, 0)
# Next Tetromino Display Position
NEXT_TETROMINO_OFFSET = vec((WIDTH - GRID_WIDTH) //
                            2, HEIGHT // 4 + GRID_WIDTH)
NEXT_TEXT_POS = WIDTH - HUD_WIDTH // 2, HEIGHT // 8  # Next Text Display Position
SCORE_TEXT_POS = WIDTH - HUD_WIDTH // 2, HEIGHT // 2  # Score Text Display Position
SCORE_POS = WIDTH - HUD_WIDTH // 2, HEIGHT * 5 // 8  # Score Display Position
# Level Text Display Position
LEVEL_TEXT_POS = WIDTH - HUD_WIDTH // 2, HEIGHT * 3 // 4
LEVEL_POS = WIDTH - HUD_WIDTH // 2, HEIGHT * 7 // 8  # Level Display Position
GAMENAME_HEIGHT = 150  # Game Name Height
MANUAL_HUD_POS = 110, 450  # Manual HUD Position
GAMEMESSAGE_HEIGHT = 300  # Game Message Height
SCOREMESSAGE_HEIGHT = 400  # Score Message Heigh

# Font Path
TITLE_FONT = pg.font.Font('assets/font/Red October.ttf', 120)
GAME_FONT = pg.font.Font('assets/font/Red October.ttf', 40)

# Game Events
FALL_TRIGGER = pg.USEREVENT + 1  # Tetrimino Fall
ANIM_TRIGGER = pg.USEREVENT + 2  # Tetrimino Animation
FAST_FALL_TRIGGER = pg.USEREVENT + 3  # Tetrimino Fast Fall
NEXT_MUSIC = pg.USEREVENT + 4  # Next Music

# Event Frequence and Delay Time
FALL_FREQ = 500  # Tetrimino Fall Frequency
ANIM_TRIGGER_FREQ = 100  # Tetrimino Animation Frequency
FAST_FALL_FREQ = 15  # Tetrimino Fast Fall Frequency

GAMEOVER_DELAY = 3000  # Game Over Delay

# Image Path
TETROMINO_TILES = 'assets/tetrominos/tetromino_tiles.png'
BACKGROUND_IMAGE = 'assets/hud/Tetris Background.png'
MANUAL_HUD = 'assets/hud/manual.png'

TETROMINO_TILETYPE = {
    'O': 0,
    'T': 1,
    'S': 2,
    'Z': 3,
    'J': 4,
    'L': 5,
    'I': 6
}

# Sound Path
PREGAME_MUSIC = 'assets/sound/Korobeiniki.mp3'
GAMEOVER_MUSIC = 'assets/sound/sndGameOver.ogg'
LINE_CLEAR_SOUND = 'assets/sound/sndLineClear.ogg'
FOURLINE_CLEAR_SOUND = 'assets/sound/sndFourLinesClear.ogg'
ROTATE_SOUND = 'assets/sound/sndRotate.ogg'
FALL_SOUND = 'assets/sound/sndFall.ogg'
LEVELUP_SOUND = 'assets/sound/sndLevelUp.ogg'
LANDING_SOUND = 'assets/sound/sndTetronimoLanding.ogg'

# Tetromino Shapes
TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (-1, 0), (-1, -1), (0, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (-1, -1), (0, -1)]
}

TETROMINO_ROTATIONS = {
    'O': [
        [(0, 0), (-1, 0), (-1, -1), (0, -1)]  # 0 degrees
    ],

    'T': [
        [(0, 0), (-1, 0), (1, 0), (0, -1)],   # 0 degrees
        [(0, 0), (0, 1), (0, -1), (-1, 0)],   # 90 degrees
        [(0, 0), (1, 0), (-1, 0), (0, 1)],    # 180 degrees
        [(0, 0), (0, -1), (0, 1), (1, 0)]     # 270 degrees
    ],

    'S': [
        [(0, 0), (-1, 0), (0, -1), (1, -1)],  # 0 degrees
        [(0, 0), (0, 1), (-1, 0), (-1, -1)]   # 90 degrees
    ],

    'Z': [
        [(0, 0), (1, 0), (-1, -1), (0, -1)],  # 0 degrees
        [(0, 0), (0, 1), (1, -1), (1, 0)]     # 90 degrees
    ],

    'J': [
        [(0, 0), (-1, 0), (0, -1), (0, -2)],  # 0 degrees
        [(0, 0), (0, 1), (-1, 0), (-2, 0)],    # 90 degrees
        [(0, 0), (1, 0), (0, 1), (0, 2)],     # 180 degrees
        [(0, 0), (0, -1), (1, 0), (2, 0)]   # 270 degrees
    ],

    'L': [
        [(0, 0), (1, 0), (0, -1), (0, -2)],   # 0 degrees
        [(0, 0), (0, -1), (-1, 0), (-2, 0)],    # 90 degrees
        [(0, 0), (-1, 0), (0, 1), (0, 2)],    # 180 degrees
        [(0, 0), (0, 1), (1, 0), (2, 0)]   # 270 degrees
    ],

    'I': [
        [(0, 0), (0, 1), (0, -1), (0, -2)],   # 0 degrees
        [(0, 0), (-1, 0), (1, 0), (2, 0)]     # 90 degrees
    ]
}
