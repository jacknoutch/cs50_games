import pygame as pg
import random

from fiftybird.assets import assets
from fiftybird.settings import PIPE_IMAGE, PIPE_SCROLL_SPEED, VIRTUAL_WIDTH, VIRTUAL_HEIGHT

class Pipe:
    def __init__(self, orientation, y, image_path=PIPE_IMAGE):
        self.orientation = orientation
        
        # load image from assets to ensure image load only once, not per instantiation
        self.base = assets.pipe

        # flip the image if top
        if self.orientation == "top":
            self.image = pg.transform.flip(self.base, False, True)
        elif self.orientation == "bottom":
            self.image = self.base

        # create the rect with provided y 
        self.rect = self.image.get_rect()
        self.rect.topleft = (VIRTUAL_WIDTH, y)

        # keep a float x for smooth sub-pixel movement
        self.x = float(self.rect.x)
        self.y = self.rect.y

    def render(self, surface: pg.Surface):
        self.rect.x = int(self.x)
        surface.blit(self.image, self.rect.topleft)