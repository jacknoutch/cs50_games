import pygame as pg
import random

from breakout.src.settings import VIRTUAL_HEIGHT, VIRTUAL_WIDTH

BALL_WIDTH = 8
BALL_HEIGHT = 8
BALL_SPEED = 200
BALL_COLLISION_MARGIN = -2

class Ball:
    def __init__(self, surface, wall_sound):
        self.width = BALL_WIDTH
        self.height = BALL_HEIGHT
        self.colour = None
        self.surf = surface
        self.rect = self.surf.get_frect()
        self.wall_sound = wall_sound

        self.speed = BALL_SPEED
        self.velocity = pg.Vector2(0, 0)

    def update(self, dt):
        self.rect.center += self.velocity * self.speed * dt

        if self.rect.left <= 0:
            self.rect.left = 0
            self.velocity.x *= -1
            self.wall_sound.play()
        elif self.rect.right >= VIRTUAL_WIDTH:
            self.rect.right = VIRTUAL_WIDTH
            self.velocity.x *= -1
            self.wall_sound.play()
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity.y *= -1
            self.wall_sound.play()
        elif self.rect.bottom >= VIRTUAL_HEIGHT:
            self.rect.bottom = VIRTUAL_HEIGHT
            self.velocity.y *= -1
            self.wall_sound.play()

    def render(self, surface):
        surface.blit(self.surf, self.rect)

    def collide(self, other):
        """
        Check for collision with another object.
        """
        collision_rect = self.rect.inflate(BALL_COLLISION_MARGIN, BALL_COLLISION_MARGIN)
        return collision_rect.colliderect(other.rect)

    def bounce(self):
        self.velocity.y *= -1

    def reset(self):
        self.rect.center = (VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2)
        self.velocity = pg.Vector2(0, 0)

    def start(self):
        """
        Set the ball in motion at a random angle upwards.
        """
        x = random.uniform(-1, 1)
        y = random.uniform(-1, -0.5)
        self.velocity = pg.Vector2(x, y)