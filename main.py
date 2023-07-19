import pygame

from game_settings import *
from tetris import Tetris
import sys

class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Tetris')
        self.screen = pygame.display.set_mode(FIELD_RES)
        self.clock = pygame.time.Clock()
        self.tetris = Tetris(self)
        self.set_timer()

    def set_timer(self):
        self.user_events = pygame.USEREVENT + 0
        self.trigger_animation = False
        pygame.time.set_timer(self.user_events, ANIMATION_INTERVAL)


    def update_game(self):
        self.clock.tick(FPS)
        self.tetris.update()

    def draw(self):
        self.screen.fill(color=FIELD_COLOR)
        self.tetris.draw()
        pygame.display.flip()


    def check_events(self):
        #  check for events during the game, in case the users wants to move or quit the game
        self.trigger_animation = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.tetris.controls(pressed_key=event.key)
            elif event.type == self.user_events:
                self.trigger_animation = True

    def play(self):
        while True:
            self.check_events()
            self.update_game()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.play()