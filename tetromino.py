from game_settings import *

# we need to inherit from pygame in order to use the sprites for the blocks
class Block(pygame.sprite.Sprite):
    # the position of the block on the playing field using the coordinates i.e (0,3)
    def __init__(self, tetromino, position):
        self.tetromino = tetromino
        self.position = vector_2D(position) + INIT_POS
        super().__init__(tetromino.tetris.sprites)
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position * TILE_SIZE


class Tetromino:
    def __init__(self, tetris):
        self.tetris = tetris
        self.shape = 'T'
        self.blocks = [Block(self,pos) for pos in SHAPES[self.shape]]

    def update(self):
        pass


