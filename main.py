from game_settings import *
import sys


class App:
    def __init__(self):
        game.init()
        game.display.set_caption('Tetris')
        self.screen = game.display.set_mode(FIELD_RES)
        self.clock = game.time.Clock()

    def update_game(self):
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=FIELD_COLOR)
        game.display.flip()

    def check_events(self):
        for event in game.event.get():
            if event.type == game.QUIT or (event.type == game.KEYDOWN and event.key == game.K_ESCAPE):
                game.quit()
                sys.exit()

    def play(self):
        while True:
            self.check_events()
            self.update_game()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.play()