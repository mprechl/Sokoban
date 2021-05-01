# imports
import os
import pygame
from menu import Menu
from game import Game
from level_selector import Selector
from highscores import Register, Highscores


class App:
    """the main class that controls the program"""
    def __init__(self, mode=None, menu=None, game=None, selector=None, register=None, highscores=None):
        self.mode = mode
        self.menu = menu
        self.game = game
        self.highscores = highscores
        self.selector = selector
        self.register = register

    def pygame_init(self):
        """initialisation and window setup"""
        # set window position
        os.environ['SDL_VIDEO_WINDOW_POS'] = "325,15"
        # initialise pygame window
        pygame.init()
        self.window = pygame.display.set_mode((720, 720))
        pygame.display.set_caption('Sokoban')

    def draw(self):
        """draws the current screen"""
        # each class has a standard draw method that draws the corresponding screen
        [self.menu, self.game, self.register, self.selector, self.highscores][self.mode].draw(self.window)


class Mode:
    """used to simplify switching between modes"""
    menu = 0    # main menu
    game = 1    # play loaded level
    register = 2    # register new highscores
    selector = 3    # select game level to load
    highscores = 4  # display highscores for loaded level


def main():
    # create App instance in menu mode and make pygame window
    app = App(Mode.menu)
    app.pygame_init()

    # assign menu and level selector objects
    app.menu = Menu(["Continue", "Highscores", "Load"])
    # reading levels from './assets/levels'
    app.selector = Selector("./assets/levels/")

    # draw the screen
    app.draw()
    pygame.display.update()

    # main loop for user interaction
    done = False
    while not done:
        # event listener
        event = pygame.event.wait()
        # shut down program when window is closed
        if event.type == pygame.QUIT:
            done = True
        # keyboard interaction TODO? move everything to class methods
        elif event.type == pygame.KEYDOWN:
            # ESC returns to main menu from any part of the program
            if event.key == pygame.K_ESCAPE:
                app.mode = Mode.menu

            # keyboard interaction in game mode
            if app.mode == Mode.game:
                # player movement with arrows or WASD
                direction = None
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    direction = (1, 0)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    direction = (0, 1)

                if direction is not None:
                    app.game.validate_and_move(direction)
                    # if this was the finishing move, record new highscore
                    if app.game.finished:
                        app.register = Register(app.game.path, app.game.counter)
                        app.mode = Mode.register
                        # unload the level
                        app.game = None
                        app.menu.loaded = False
                        app.selector.load()
                # R resets the level
                elif event.key == pygame.K_r:
                    app.game.load()

            # keyboard interaction in menu mode
            elif app.mode == Mode.menu:
                # option selection with arrows or WASD
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    app.menu.move(-1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    app.menu.move(+1)
                # confirm selection with space or enter
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if app.menu.current == 0 and app.menu.loaded:
                        app.mode = Mode.game
                    elif app.menu.current == 1 and app.menu.loaded:
                        app.mode = Mode.highscores
                    elif app.menu.current == 2:
                        app.mode = Mode.selector

            # keyboard interaction in level selector mode
            elif app.mode == Mode.selector:
                # level selection with arrows or WASD
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    app.selector.move(-1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    app.selector.move(+1)
                # confirm selection with space or enter
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # call a method of selector that returns the selected level
                    # then create new game and highscores instance with that
                    level = app.selector.select()
                    app.game = Game(level.file)
                    app.highscores = Highscores(level.file)
                    app.menu.loaded = True

            #keyboard interaction in new highscore register mode
            elif app.mode == Mode.register:
                # returns True when name is submitted
                if app.register.key_press(event):
                    # display the highscores
                    app.highscores.find_top()
                    app.mode = Mode.highscores

            # update the screen on every keypress
            app.draw()
            pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
