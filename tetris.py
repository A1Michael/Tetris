from game_settings import *
from tetromino import Tetromino

import math

class Tetris:
    def __init__(self, game):
        self.game = game
        self.sprites = pygame.sprite.Group()  # will contain all our sprites
        self.tetromino = Tetromino(self)
        self.field_array = self.get_field_array()
    def controls(self, pressed_key):
        if pressed_key == pygame.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pygame.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pygame.K_UP or pygame.K_SPACE:
            self.tetromino.rotate()

    def check_full_lines(self):
        row = FIELD_H - 1
        # iterate through the array from bottom to top
        for y in range(FIELD_H - 1, -1, -1):
            # iterate from left to right
            for x in range(FIELD_W):
                # reassign the values of the elements in the array because the val of row is now equal to 1
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].position = vector_2D(x, y)  # ? not sure why this error is being flagged
            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1  # if the row is full then remove it
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False  # ?
                    self.field_array[row][x] = 0


    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]
    def put_blocks_in_array(self):
        # stores a pointer to the block object and also used to calculate collisions
        for block in self.tetromino.blocks:
            x, y = int(block.position.x), int(block.position.y)
            self.field_array[y][x] = block

    def check_landing(self):
        # if the block has landed we will create a new instance of Tetromino
        if self.tetromino.landed:
            self.put_blocks_in_array()
            self.tetromino = Tetromino(self)

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pygame.draw.rect(self.game.screen, 'black',
                                 (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        if self.game.trigger_animation:
            self.check_full_lines()
            self.tetromino.update()
            self.check_landing()
        self.sprites.update()

    def draw(self):
        self.draw_grid()
        self.sprites.draw(self.game.screen)
