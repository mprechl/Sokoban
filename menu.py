# imports
import pygame
from pygame import gfxdraw
from pygame import font


# GLOBALS
# colours
WHITE = (255, 255, 255)
GREY = (100, 100, 100)

# images
bg_img = pygame.image.load("./assets/docks_bg.png")
selected = pygame.image.load("./assets/selected.png")
notselected = pygame.image.load("./assets/notselected.png")


class Menu:
    """class that handles the main menu"""
    def __init__(self, options, current=0, loaded=False):
        self.options = options
        self.current = current
        self.loaded = loaded

    def draw(self, window):
        """draws the screen"""
        # set background
        window.blit(bg_img, (0, 0))

        # size of the menu options
        width = 350
        height = 100

        font = pygame.font.SysFont('3ds', 32)

        # throw error if too many menu options given
        if len(self.options) > 4:
            raise Exception("Too many menu options.")

        left = (720 - width) // 2
        for index, option in enumerate(self.options):
            top = 100 + 150 * index
            # if no level is loaded grey out continue and highscores options
            col = GREY if not self.loaded and index <= 1 else WHITE
            button = selected if index == self.current else notselected
            # button
            window.blit(button, (left, top))
            # text
            text = font.render(option, True, col)
            window.blit(text, (left + width // 2 - text.get_width() // 2, top + height // 2 - text.get_height() // 2))

    def move(self, direction):
        """moves the menu selection"""
        to = self.current + direction
        to = len(self.options) - 1 if to == -1 else to
        to = 0 if to == len(self.options) else to

        self.current = to
