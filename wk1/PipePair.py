import pygame as pg

from wk1.settings import PIPE_GAP, PIPE_HEIGHT, PIPE_SCROLL_SPEED, PIPE_WIDTH, VIRTUAL_WIDTH
from wk1.Pipe import Pipe

class PipePair:
    def __init__(self, x:int = VIRTUAL_WIDTH + 32, y:int = 0):
        self.x = float(x) # Needed for smooth movement because rect stores integer coordinates
        self.y = y
        self.top_pipe = Pipe("top", self.y)
        self.bottom_pipe = Pipe("bottom", self.y + PIPE_HEIGHT + PIPE_GAP)
        self.remove = False

    def update(self, dt):
        if self.x > - PIPE_WIDTH:
            self.x += PIPE_SCROLL_SPEED * dt
            self.top_pipe.x = self.x
            self.bottom_pipe.x = self.x
        else:
            self.remove = True

    def render(self, surface):
        self.top_pipe.render(surface)
        self.bottom_pipe.render(surface)