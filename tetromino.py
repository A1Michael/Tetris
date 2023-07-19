import random
from game_settings import *

# we need to inherit from pygame in order to use the sprites for the blocks
class Block(pygame.sprite.Sprite):
    # the position of the block on the playing field using the coordinates i.e (0,3)
    def __init__(self, tetromino, position):
        self.tetromino = tetromino
        self.position = vector_2D(position) + INIT_POS
        self.next_tetris_pos = vector_2D(position) + NEXT_POS
        super().__init__(tetromino.tetris.sprites)
        self.image = tetromino.image
        #self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        #pygame.draw.rect(self.image, 'blue', (1, 1, TILE_SIZE - 2, TILE_SIZE -2), border_radius=8)
        self.rect = self.image.get_rect()
        self.alive = True
        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)
        self.sfx_speed = random.uniform(0.2, 0.6)
        self.sfx_cycles = random.randrange(6, 8)
        self.cycle_counter = 0

    def sfx_end(self):
        if self.tetromino.tetris.game.anim_trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True
    def run_sfx(self):
        self.image = self.sfx_image
        self.position.y = self.sfx_speed
        self.image = pygame.transform.rotate(self.image, pygame.time.get_ticks() * self.sfx_speed)


    def is_alive(self):
        if not self.alive:
            if not self.sfx_end():
                self.run_sfx()
            else:
                self.kill()

    def set_rect_pos(self):
        position = [self.next_tetris_pos, self.position][self.tetromino.current]
        self.rect.topleft = position * TILE_SIZE

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
    def __init__(self, tetris, current_tetris=True):
        self.tetris = tetris
        self.shape = random.choice(list(SHAPES.keys()))
        self.image = random.choice(tetris.game.sprite) # ...
        self.blocks = [Block(self,pos) for pos in SHAPES[self.shape]]
        self.landed = False
        self.current = current_tetris


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
