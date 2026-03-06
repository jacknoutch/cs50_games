import pygame as pg

from settings import GRAVITY, VIRTUAL_WIDTH, VIRTUAL_HEIGHT

class Bird:

    def __init__(self):
        self.image = pg.image.load("assets/bird.png").convert()
        self.rect = self.image.get_rect()
        self.dy = 0

        self.rect.topleft = (
            VIRTUAL_WIDTH // 2 - self.image.get_width() // 2,
            VIRTUAL_HEIGHT // 2 - self.image.get_height() // 2
        )

    def render(self, surface: pg.Surface):
        surface.blit(self.image, self.rect.topleft)

    def update(self, dt: float, keys_pressed: pg.key.ScancodeWrapper):
        """
        Update the bird's position and velocity based on the game's gravity.
        """
        self.dy += GRAVITY * dt
        self.rect.y += self.dy

        if keys_pressed[pg.K_SPACE]:
            self.jump(dt)

    def jump(self, dt: float):
        """
        Make the bird jump by applying an upward velocity.
        """
        self.dy = -300 * dt
