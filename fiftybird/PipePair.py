import pygame as pg

from fiftybird.settings import PIPE_GAP, PIPE_HEIGHT, PIPE_SCROLL_SPEED, PIPE_WIDTH, VIRTUAL_WIDTH
from fiftybird.Pipe import Pipe

class PipePair:
    def __init__(self, x:int = None, y:int = 0):

        self.scored = False

        # initialise pipe past the right edge of the screen
        self.x = float(x) if x is not None else VIRTUAL_WIDTH + 32

        # y is the value of the top pipe's y-coordinate
        self.y = y

        # create pipe objects
        self.pipes = {
            "top": Pipe("top", self.y),
            "bottom": Pipe("bottom", self.y + PIPE_HEIGHT + PIPE_GAP)
        }

        # flag to mark pipe for removal
        self.remove = False
        

    def update(self, dt):
        # update the position of the pipe pair
        self.x += PIPE_SCROLL_SPEED * dt
        self.pipes["top"].x = self.x
        self.pipes["bottom"].x = self.x

        # flag for removal if the pipe is off screen to the left
        if self.x <= -PIPE_WIDTH:
            self.remove = True

            
    def render(self, surface):
        # render each of the pipes in turn
        self.pipes["top"].render(surface)
        self.pipes["bottom"].render(surface)