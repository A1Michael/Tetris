import random

from game_settings import *

# we need to inherit from pygame in order to use the sprites for the blocks
class Block(pygame.sprite.Sprite):
    # the position of the block on the playing field using the coordinates i.e (0,3)
    def __init__(self, tetromino, position):
        super().__init__(tetromino.tetris.sprites)
        self.tetromino = tetromino
        self.position = vector_2D(position) + INIT_POS
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        pygame.draw.rect(self.image, 'blue', (1, 1, TILE_SIZE - 2, TILE_SIZE -2), border_radius=8)
        self.rect = self.image.get_rect()
        self.alive = True

    def is_alive(self):
        if not self.alive:
            self.kill()

    def set_rect_pos(self):
        self.rect.topleft = self.position * TILE_SIZE

    def rotate(self, pivot_point):
        translated = self.position - pivot_point
        rotated = translated.rotate(90)
        return rotated + pivot_point

    def is_colliding(self , pos):
        # checks if the x and y cordinates are touching the edge of the field
        # if the block is within bounds then we return false
        # also check for additional blocks in the array
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (
                y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True

    #this will update the blocks position and allow it to move
    def update(self):
        self.is_alive()
        self.set_rect_pos()


class Tetromino:
    def __init__(self, tetris):
        self.tetris = tetris
        self.shape = random.choice(list(SHAPES.keys()))
        self.blocks = [Block(self,pos) for pos in SHAPES[self.shape]]
        self.landed = False

    def is_colliding(self, block_pos):
        # we will be performing the check on all four tetris blocks
        # using the map function we will call a collision check for each block
        return any(map(Block.is_colliding, self.blocks, block_pos))

    def rotate(self):
        pivot_posistion = self.blocks[0].position
        new_block_position = [block.rotate(pivot_posistion) for block in self.blocks]
        if not self.is_colliding(new_block_position):
            for i, block in enumerate(self.blocks):
                block.position = new_block_position[i]
    def move(self, direction):
        # function holds the movement of the blocks
        movement_dir = MOVEMENT_DIR[direction]
        new_block_position = [block.position + movement_dir for block in self.blocks]
        is_colliding = self.is_colliding(new_block_position)

        if not is_colliding:
            for block in self.blocks:
                block.position += movement_dir
        elif direction == 'down':
            # once the block lands
            self.landed = True

    def update(self):
        self.move(direction='down')
