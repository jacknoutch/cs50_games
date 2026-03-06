import pygame as pg
import random

from settings import PIPE_IMAGE, VIRTUAL_WIDTH, VIRTUAL_HEIGHT


pipe_scroll = -60

class Pipe:
    def __init__(self, image_path=PIPE_IMAGE):
        self.image = pg.image.load(image_path).convert()
        self.x = float(VIRTUAL_WIDTH) # Needed for smooth movement because rect stores integer coordinates 
        self.rect = self.image.get_rect()

        self.rect.topleft = (
            VIRTUAL_WIDTH,
            random.randint(VIRTUAL_HEIGHT // 4, VIRTUAL_HEIGHT - 30)
        )

    def update(self, dt: float):
        self.x += pipe_scroll * dt
        self.rect.x = int(self.x) # Setting rect.x directly would result in jittery movement

    def render(self, surface: pg.Surface):
        surface.blit(self.image, self.rect.topleft)