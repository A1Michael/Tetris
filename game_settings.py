import pygame

FPS = 60
FIELD_COLOR = (48, 39, 32)
vector_2D = pygame .math.Vector2
TILE_SIZE = 50
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE
SPRITES_DIRECTORY = 'Tetris/Assests/Sprites'
FONT_PATH = 'Tetris/Assests/Texts/FREAKSOFNATUREMASSIVE.ttf'
FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WINDOW_RES = WINDOW_W, WINDOW_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H
BACKGROUND_COLOR = (32, 69, 117)


# Dictionary of block shapes
SHAPES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)],
}

# Initial pos will be used to place the block in the middle of the field
INIT_POS = vector_2D(FIELD_W // 2 - 1, 0)
NEXT_POS = vector_2D(FIELD_W * 1.3, FIELD_H * 0.45)

# Since we can only move left, right and down. we only need 3 direction represented using vector coordinates
MOVEMENT_DIR = {'left': vector_2D(-1, 0), 'right': vector_2D(1, 0), 'down': vector_2D(0, 1)}
ANIMATION_INTERVAL = 150  # in milliseconds
FAST_ANIMATION_INTERVAL = 15 # the speed at which the block will drop down when 'down' is pressed

