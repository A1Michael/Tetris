from game_settings import *
from tetromino import Tetromino
import pygame.freetype as ft
import math

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def get_color(self):
        time = pygame.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    def draw(self):
        self.font.render_to(self.app.screen, (WINDOW_W * 0.595, WINDOW_H * 0.02),
                            text='TETRIS', fgcolor=self.get_color(),
                            size=TILE_SIZE * 1.65, bgcolor='black')
        self.font.render_to(self.app.screen, (WINDOW_W * 0.65, WINDOW_H * 0.22),
                            text='next', fgcolor='orange',
                            size=TILE_SIZE * 1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (WINDOW_W * 0.64, WINDOW_H * 0.67),
                            text='score', fgcolor='orange',
                            size=TILE_SIZE * 1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (WINDOW_W * 0.64, WINDOW_H * 0.8),
                            text=f'{self.app.tetris.score}', fgcolor='white',
                            size=TILE_SIZE * 1.8)
class Tetris:
    def __init__(self, game):
        self.game = game
        self.sprites = pygame.sprite.Group()  # will contain all our sprites
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current_tetris=False)
        self.field_array = self.get_field_array()
        self.drop_fast = False
        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

    def controls(self, pressed_key):
        if pressed_key == pygame.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pygame.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pygame.K_UP or pressed_key == pygame.K_SPACE:

            self.tetromino.rotate()
        elif pressed_key == pygame.K_DOWN:
            self.drop_fast = True

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
                self.full_lines += 1


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
            if self.is_game_over():
                self.__init__(self.game)
            else:

                self.drop_fast = False
                self.put_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current_tetris=False)

    def is_game_over(self):
        if self.tetromino.blocks[0].position.y == INIT_POS[1]:
            pygame.time.wait(300)
            return True

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pygame.draw.rect(self.game.screen, 'black',
                                 (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        trigger = [self.game.trigger_animation, self.game.trigger_fast_animation][self.drop_fast]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.get_score()
            self.check_landing()
        self.sprites.update()

    def draw(self):
        self.draw_grid()
        self.sprites.draw(self.game.screen)
