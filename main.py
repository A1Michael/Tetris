import pygame

from game_settings import *
from tetris import Tetris, Text
import sys
import pathlib

class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Tetris')
        self.screen = pygame.display.set_mode(WINDOW_RES)
        self.clock = pygame.time.Clock()
        self.set_timer()
        self.sprite = self.load_sprites()
        self.tetris = Tetris(self)
        self.text = Text(self)



    def load_sprites(self):
        # first get all the png file names
        files = [item for item in pathlib.Path(SPRITES_DIRECTORY).rglob('*.png') if item.is_file()]
        sprites = [pygame.image.load(file).convert_alpha() for file in files]
        sprites = [pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE)) for sprite in sprites]
        return sprites

    def set_timer(self):
        self.user_events = pygame.USEREVENT + 0
        self.fast_user_events = pygame.USEREVENT + 1
        self.trigger_animation = False
        self.trigger_fast_animation = False
        pygame.time.set_timer(self.user_events, ANIMATION_INTERVAL)
        pygame.time.set_timer(self.fast_user_events, FAST_ANIMATION_INTERVAL)

    def update_game(self):
        self.clock.tick(FPS)
        self.tetris.update()

    def draw(self):
        self.screen.fill(color=BACKGROUND_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, * FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pygame.display.flip()


    def check_events(self):
        #  check for events during the game, in case the users wants to move or quit the game
        self.trigger_animation = False
        self.trigger_fast_animation = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.tetris.controls(pressed_key=event.key)
            elif event.type == self.user_events:
                self.trigger_animation = True
            elif event.type == self.fast_user_events: # hmm
                self.trigger_fast_animation = True


    def play(self):
        while True:
            self.check_events()
            self.update_game()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.play()