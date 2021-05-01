# imports
import os
import pygame
from pygame import gfxdraw
from pygame import font
from game import Game


# GLOBALS
# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (100, 100, 100)
BROWN = (64, 19, 19)
BLUE = (66, 135, 245)
PURPLE = (255, 0, 193)

# images
bg_img = pygame.image.load("./assets/docks_bg.png")
outline = pygame.image.load("./assets/selector_outline.png")


class Selector:
    """level selection menu screen"""
    def __init__(self, folder, current=0, pagenum=0):
        self.folder = folder
        self.current = current
        self.pagenum = pagenum

        # load up levels on creation
        self.load()

    def load(self):
        """loads up the game level files from given folder"""
        # create list of Unit objects from all level files in the folder
        unitlist = []
        dirlist = os.scandir(self.folder)
        for entry in dirlist:
            # only load xsb files
            if entry.is_file() and entry.name.endswith(".xsb"):
                unitlist.append(Unit(entry.path))

        # separate the list into pages for easier display
        pages = []
        for i in range(len(unitlist) // 6 + 1):
            page = []
            for j in range(6):
                try:
                    page.append(unitlist[i * 6 + j])
                except IndexError:
                    break
            pages.append(page)
        self.pages = pages

    def draw(self, window):
        """draws the screen"""
        # set background
        window.blit(bg_img, (0, 0))

        # create foreground
        fg = pygame.Surface((600, 600))
        fg.fill(BLACK)

        # draw each level file entry of the page
        for index, unit in enumerate(self.pages[self.pagenum]):
            # entry surface needs to be regenerated for display
            unit.surface_generator()
            # mark selected entry w/ black and yellow outline
            if index == self.current:
                unit.surface.blit(outline, (0, 0))
            fg.blit(unit.surface, (0, index*100))

        # draw foreground to window
        window.blit(fg, (60, 60))


    def move(self, direction):
        """move the selection up/down"""
        # direction parameter: +1 -> down, -1 -> up
        to = self.current + direction

        # deal w/ over and underflow, page flip
        if to == -1:
            if self.pagenum - 1 >= 0:
                to = 5
                self.pagenum -= 1
            else:
                to = 0
        if to == 6:
            if self.pagenum + 1 <= len(self.pages) - 1:
                to = 0
                self.pagenum += 1
            else:
                to = 5

        # deal with last page
        if self.pagenum == len(self.pages) - 1:
            if to == len(self.pages[self.pagenum]):
                to = len(self.pages[self.pagenum]) - 1

        self.current = to

    def select(self):
        """confirm level selection and return the selected level file"""
        # first unselect everything
        for page in self.pages:
            for unit in page:
                unit.selected = False
        # then set selected flag of the entry for display purposes
        self.pages[self.pagenum][self.current].selected = True
        # return the selected level file
        return self.pages[self.pagenum][self.current]

class Unit:
    """a menu entry for the level selector"""
    def __init__(self, file, selected=False):
        self.file = file
        self.selected = selected

        # generate thumbnail and entry surface on creation
        self.thumbnail_generator()
        self.surface_generator()

    def surface_generator(self):
        """generates complete menu entry surface"""
        surf = pygame.Surface((600, 100))
        # the selected entry gets blue background
        bg = BLUE if self.selected else BLACK
        surf.fill(bg)
        # thumbnail on right edge
        surf.blit(self.thumb, (500, 0))
        pygame.gfxdraw.rectangle(surf, pygame.Rect(0, 0, 600, 100), WHITE)

        # level file name on left side
        font = pygame.font.SysFont('3ds', 32)
        text = font.render(self.file.split("/")[-1], True, WHITE)
        surf.blit(text, (20, 20))

        self.surface = surf

    def thumbnail_generator(self):
        """generates a preview thumbnail of a level as a surface"""
        # create surface 100x100px thumbnail for 20x20 level at 5:1 scale
        thumb = pygame.Surface((100, 100))
        # set background
        thumb.fill(BROWN)

        # read the level file
        level = Game.read_xsb(self, self.file)

        # determine level size
        w = max([len(i) for i in level])
        h = len(level)

        # check if the level is within the 20x20 level size limit
        # beacause every level runs through this we don't need to check elsewhere
        if w > 20 or h > 20:
            raise Exception("Level at {} is too large.".format(self.file))

        # position the playing field in middle of thumbnail
        left = (20 - w) // 2
        top = (20 - h) // 2

        # draw the thumbnail
        for y, row in enumerate(level):
            for x, symbol in enumerate(row):
                col = None
                if symbol == "#":
                    col = GREY
                elif symbol == ".":
                    col = RED
                elif symbol == "@":
                    col = BLUE
                elif symbol == "+":
                    col = PURPLE
                elif symbol == "$":
                    col = BLACK
                elif symbol == "*":
                    col = GREEN

                if col != None:
                    pygame.gfxdraw.box(thumb, pygame.Rect((left + x)*5, (top + y)*5, 5, 5), col)

        self.thumb = thumb
