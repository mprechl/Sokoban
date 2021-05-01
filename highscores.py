# imports
import string
from operator import itemgetter
from time import sleep
import pygame
from pygame import gfxdraw
from pygame import font


# GLOBALS
# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# images
bg_img = pygame.image.load("./assets/docks_bg.png")


class Register:
    """the screen where users can save their scores when they finish a level"""
    def __init__(self, levelfile, score):
        self.levelfile = levelfile
        self.score = score

        # start with empty name string
        self.name_str = ""

    def draw(self, window):
        """draws the screen"""
        # set background
        window.blit(bg_img, (0, 0))

        # create foreground surface
        fg = pygame.Surface((600, 600))
        fg.fill(BLACK)
        pygame.gfxdraw.rectangle(fg, pygame.Rect(0, 0, 600, 600), WHITE)

        # create texts and put them on foreground
        font = pygame.font.SysFont('3ds', 32)
        texts = []
        texts.append(font.render("FINISHED!", True, WHITE))
        texts.append(font.render("Number of moves: " + str(self.score), True, WHITE))
        texts.append(font.render("Enter your name:", True, WHITE))
        texts.append(font.render("{:_<10}".format(self.name_str), True, WHITE))
        texts.append(font.render("(Leave empty or press ESC to discard..)", True, WHITE))
        for index, text in enumerate(texts):
            # align texts to centre
            fg.blit(text, (300 - text.get_width()/2, (index + 1) * 30))

        # draw foreground to window
        window.blit(fg, (60, 60))

    def save_to_file(self):
        """saves the score to a file corresponding to the level's file name"""
        # make sure a name was given
        if len(self.name_str) > 0:
            # file is saved in './assets/highscores/[levelname].txt'
            # where each line is: '[name] [score]\n'
            dest = self.levelfile.replace("levels", "highscores").replace(".xsb", ".txt")
            with open(dest, "at") as f:
                f.write(self.name_str + " " + str(self.score) + "\n")

    def key_press(self, event):
        """deal with text input, returns True when name is submitted"""
        # enter to save score and display highscores
        if event.key == pygame.K_RETURN:
            self.save_to_file()
            return True
        # name input
        elif event.key == pygame.K_BACKSPACE:
            self.name_str = self.name_str[:-1]
        else:
            # name is latin alphabet uppercase only
            if event.unicode in string.ascii_letters and len(self.name_str) < 10:
                self.name_str += event.unicode.upper()

        return False


class Highscores:
    """screen that displays the highscores for a game level"""
    def __init__(self, levelfile):
        self.levelfile = levelfile

        # generate the toplist on creation
        self.find_top()

    def draw(self, window):
        """draws the screen"""
        # set background
        window.blit(bg_img, (0, 0))

        # create foreground surface
        fg = pygame.Surface((600, 600))
        fg.fill(BLACK)
        pygame.gfxdraw.rectangle(fg, pygame.Rect(0, 0, 600, 600), WHITE)

        # draw the topscores
        font = pygame.font.SysFont('3ds', 32)
        for index, entry in enumerate(self.top):
            # render name and score separately beacause it doesn't handle string formatting
            name_text = font.render(entry[0], True, WHITE)
            fg.blit(name_text, (50, 50 + index*50))
            score_text = font.render(str(entry[1]), True, WHITE)
            fg.blit(score_text, (400, 50 + index*50))

        # draw foreground to window
        window.blit(fg, (60, 60))

    def find_top(self):
        """read highscore file and make a list w/ the top 10 scores and names"""
        file = self.levelfile.replace("levels", "highscores").replace(".xsb", ".txt")
        try:
            with open(file, "rt") as f:
                entries = [line.rstrip("\n").split(" ") for line in f.readlines()]
            entries = [[entry[0], int(entry[1])] for entry in entries]
            # sort the highscore entries by score ascending
            entries = sorted(entries, key=itemgetter(1))
        except FileNotFoundError:
            # display when there is no highscore file for the level
            # this is the easiest way to display it like it's a top score
            entries = [["No available highscores yet", ""]]

        #only show top 10 scores
        self.top = entries[:10]
