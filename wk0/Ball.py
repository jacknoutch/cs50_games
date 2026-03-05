import pygame as pg
import random

from settings import *

class Ball:
    def __init__(self, x, y, width=BALL_SIZE, height=BALL_SIZE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dx = 100 if random.randint(0, 1) == 0 else -100
        self.dy = random.randint(-50, 50)

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

        if self.y <= 0 or self.y >= VIRTUAL_HEIGHT - self.height:
            self.dy *= -1

    def render(self, surface):
        pg.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height))

    def collides(self, paddle):
        if self.x > paddle.x + paddle.width or paddle.x > self.x + self.width:
            return False

        if self.y > paddle.y + paddle.height or paddle.y > self.y + self.height:
            return False

        return True
    
    def reset(self):
        self.x = VIRTUAL_WIDTH // 2 - BALL_SIZE // 2
        self.y = VIRTUAL_HEIGHT // 2 - BALL_SIZE // 2
        self.dx = 100 if random.randint(0, 1) == 0 else -100
        self.dy = random.randint(-50, 50)
