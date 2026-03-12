import pygame as pg

from breakout.src.settings import VIRTUAL_HEIGHT, VIRTUAL_WIDTH

PADDLE_SPEED = 200

class Paddle:

    def __init__(self, color, size, surface):
        self.color = color
        self.size = size
        self.surface = surface

        self.rect = self.surface.get_frect()
        self.rect.center = (VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT - 50)

        self.speed = PADDLE_SPEED
        self.direction = 1
        self.velocity = pg.math.Vector2(0)

    def update(self, dt):
        self.rect.center += self.velocity * self.speed * dt

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= VIRTUAL_WIDTH:
            self.rect.right = VIRTUAL_WIDTH

    def render(self, surface):
        surface.blit(self.surface, self.rect)

    def move(self, dx):
        self.velocity = pg.math.Vector2(dx, 0)

    def stop(self):
        self.velocity = pg.math.Vector2(0, 0)
