from game_settings import *
from tetromino import Tetromino
import math

class Tetris:
    def __init__(self, game):
        self.game = game
        self.sprites = pygame.sprite.Group()  # will contain all our sprites
        self.tetromino = Tetromino(self)


    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pygame.draw.rect(self.game.screen, 'black',
                                 (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    print('finished')
    def update(self):
        self.tetromino.update()
        self.sprites.update()

    def draw(self):
        self.draw_grid()
        self.sprites.draw(self.game.screen)
