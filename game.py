#imports
import pygame


# GLOBALS
# colours
WHITE = (255, 255, 255)

# images
crate = pygame.image.load("./assets/crate.png")
wall = pygame.image.load("./assets/wall.png")
player = pygame.image.load("./assets/player.png")
ground_bg = pygame.image.load("./assets/ground_bg.png")
ground_tile = pygame.image.load("./assets/ground_tile.png")
red_overlay = pygame.image.load("./assets/red_overlay.png")


class Game:
    """class that handles game logic and graphics"""
    def __init__(self, path, finished=False):
        self.path = path
        self.finished = finished

        # load the level on creation
        self.load()

    def load(self):
        # read a level from file
        level = self.read_xsb(self.path)
        # separate static and dynamic parts of the level
        self.static_level, self.player_pos, self.crate_positions = self.extract_static_level(level)

        # determine level size
        w = max([len(i) for i in level])
        h = len(level)

        # position the playing field in middle of window
        left = (720/36 - w) // 2
        top = (720/36 - h) // 2
        self.topleft = (left, top)

        # reset move counter
        self.counter = 0


    def read_xsb(self, path):
        """reads the level file"""
        with open(path, "r") as f:
            lines = [list(x.rstrip("\n")) for x in f.readlines()]

        return lines

    def extract_static_level(self, level):
        """separates the static and dynamic parts of the level"""
        player_pos = None
        crate_positions = []
        # make deep copy
        stat = [list(i) for i in level]
        for y, row in enumerate(stat):
            for x, symbol in enumerate(row):
                if symbol == "@":
                    player_pos = (x, y)
                    stat[y][x] = " "
                elif symbol == "+":
                    player_pos = (x, y)
                    stat[y][x] = "."
                elif symbol == "$":
                    crate_positions.append((x, y))
                    stat[y][x] = " "
                elif symbol == "*":
                    crate_positions.append((x, y))
                    stat[y][x] = "."
        return stat, player_pos, crate_positions

    def draw_static_level(self, window):
        """draws the static level on the screen"""
        left, top = self.topleft[0], self.topleft[1]
        for y, row in enumerate(self.static_level):
            for x, symbol in enumerate(row):
                if symbol == "#":
                    window.blit(wall, ((left + x)*36, (top + y)*36))
                elif symbol == ".":
                    window.blit(red_overlay, ((left + x)*36, (top + y)*36))

        # draw instructions
        font = pygame.font.SysFont('3ds', 32)
        text_string = "ESC - return to menu | R - restart | MOVES:" + str(self.counter)
        text = font.render(text_string, True, WHITE)
        window.blit(text, (0, 0))

    def draw_dynamic(self, window):
        """draws the player and crates"""
        # player
        x, y = self.player_pos[0], self.player_pos[1]
        window.blit(player, ((self.topleft[0] + x)*36, (self.topleft[1] + y)*36))

        # crates
        for pos in self.crate_positions:
            x, y = pos[0], pos[1]
            window.blit(crate, ((self.topleft[0] + x)*36, (self.topleft[1] + y)*36))

    def draw(self, window):
        """draws the screen"""
        # exists so all screen objects have a standard draw method
        window.blit(ground_bg, (0, 0))
        self.draw_dynamic(window)
        self.draw_static_level(window)

    def validate_and_move(self, direction):
        """checks if a move is valid and makes the move if it is,
        also checks if the game is finished after a valid move"""
        goal = (self.player_pos[0] + direction[0], self.player_pos[1] + direction[1])
        behind = (self.player_pos[0] + 2*direction[0], self.player_pos[1] + 2*direction[1])

        # simple move
        if goal not in self.crate_positions and (self.static_level[goal[1]][goal[0]] == " " or self.static_level[goal[1]][goal[0]] == "."):
            self.player_pos = (self.player_pos[0] + direction[0], self.player_pos[1] + direction[1])
            self.counter += 1
            self.check_finished()
        # push crate
        elif goal in self.crate_positions and behind not in self.crate_positions and self.static_level[behind[1]][behind[0]] != "#":
            self.player_pos = (self.player_pos[0] + direction[0], self.player_pos[1] + direction[1])
            self.crate_positions[self.crate_positions.index(goal)] = behind
            self.counter += 1
            self.check_finished()

    def check_finished(self):
        """checks whether the game is finished = all crates are on target"""
        finished = True
        for y, row in enumerate(self.static_level):
            for x, symbol in enumerate(row):
                if symbol == ".":
                    if (x, y) not in self.crate_positions:
                        finished = False
                        break

        self.finished = finished
