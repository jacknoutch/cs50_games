import pygame as pg

from settings import VIRTUAL_WIDTH, VIRTUAL_HEIGHT

class Bird:

    def __init__(self):
        self.image = pg.image.load("assets/bird.png").convert()
        self.rect = self.image.get_rect()

        self.rect.topleft = (
            VIRTUAL_WIDTH // 2 - self.image.get_width() // 2,
            VIRTUAL_HEIGHT // 2 - self.image.get_height() // 2
        )

    def render(self, surface):
        surface.blit(self.image, self.rect.topleft)