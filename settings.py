import pygame as pg
pg.init()

"""
The settings module for the "Tetris" game. This module contains all the default settings for the gameplay. 
These settings can be easily accessed and used throughout the game by importing the module into the main game file.
"""

# Game Play Settings
FPS = 30
MOVING_SPEED = 30
FRAME_INCREMENT = 1

# Game Dimensions
WIDTH, HEIGHT = 440, 600  # Game Window Display Dimensions
HUD_WIDTH, HUD_HEIGHT = 140, 600  # HUD Dimensions
GRID_WIDTH = 30  # Grid Width
ROW_NUMBER = HEIGHT // GRID_WIDTH  # Row Number
COLUMN_NUMBER = (WIDTH - HUD_WIDTH) // GRID_WIDTH  # Column Number
TETRIMINO_SPAWN_POS = (120, 0)

TETRIMINO_DIMENSIONS = {
    'I': (120, 30),
    'J': (90, 60),
    'L': (90, 60),
    'O': (60, 60),
    'S': (90, 60),
    'T': (90, 60),
    'Z': (90, 60)
}

# Font Path

# Game Events
TETRIMINO_LOCKED = pg.USEREVENT + 1

# Spawn Frequence and Delay Time

# Image Path
TETRIMINOS = {
    'I': 'assets/tetriminos/I tetrimino.png',
    'J': 'assets/tetriminos/J tetrimino.png',
    'L': 'assets/tetriminos/L tetrimino.png',
    'O': 'assets/tetriminos/O tetrimino.png',
    'S': 'assets/tetriminos/S tetrimino.png',
    'T': 'assets/tetriminos/T tetrimino.png',
    'Z': 'assets/tetriminos/Z tetrimino.png'
}

# Sound Path


# The relative positions for each rotation of the Tetrimino types.
# The values represent the relative (x, y) coordinates for each block
# in the Tetrimino, with respect to the center block.
TETRIMINO_ROTATIONS = {
    'I': [
        [(-1, 0), (0, 0), (1, 0), (2, 0)],
        [(1, -1), (1, 0), (1, 1), (1, 2)]
    ],
    'O': [
        [(0, 0), (0, 1), (1, 0), (1, 1)]
    ],
    'J': [
        [(-1, 1), (-1, 0), (0, 0), (1, 0)],
        [(0, -1), (1, -1), (0, 0), (0, 1)],
        [(1, -1), (1, 0), (0, 0), (-1, 0)],
        [(0, 1), (-1, 1), (0, 0), (0, -1)]
    ],
    'L': [
        [(-1, 0), (0, 0), (1, 0), (1, 1)],
        [(0, -1), (0, 0), (0, 1), (1, 1)],
        [(1, 0), (0, 0), (-1, 0), (-1, -1)],
        [(0, 1), (0, 0), (0, -1), (-1, -1)]
    ],
    'S': [
        [(0, 0), (1, 0), (-1, 1), (0, 1)],
        [(0, 0), (0, 1), (1, -1), (1, 0)]
    ],
    'T': [
        [(-1, 0), (0, 0), (1, 0), (0, 1)],
        [(0, -1), (0, 0), (0, 1), (1, 0)],
        [(1, 0), (0, 0), (-1, 0), (0, -1)],
        [(0, 1), (0, 0), (0, -1), (-1, 0)]
    ],
    'Z': [
        [(-1, 0), (0, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, -1)]
    ]
}
