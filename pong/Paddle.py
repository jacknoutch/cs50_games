import pygame as pg

from settings import *

class Paddle:
    def __init__(self, x, y, speed=PADDLE_SPEED, width=PADDLE_WIDTH, height=PADDLE_HEIGHT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dy = speed

    def update(self, direction=1, dt=0):
        self.y += self.dy * direction * dt
        self.y = max(0, min(VIRTUAL_HEIGHT - self.height, self.y))

    def render(self, surface):
        pg.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height))
