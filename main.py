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


    def update_game(self):
        self.clock.tick(FPS)
        self.tetris.update()

    def draw(self):
        self.screen.fill(color=FIELD_COLOR)
        self.tetris.draw()
        pygame.display.flip()


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def play(self):
        while True:
            self.check_events()
            self.update_game()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.play()