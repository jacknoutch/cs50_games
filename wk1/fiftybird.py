import pygame as pg

from settings import *
from utils import compute_letterbox

# INITIALISATION

pg.init()

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.RESIZABLE)

pg.display.set_caption("Fifty Bird")

game_surface = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

clock = pg.time.Clock()

## Images

background_image = pg.image.load("assets/background.png").convert()
ground_image = pg.image.load("assets/ground.png").convert()

running = True

while running:

    dt = clock.tick(FPS) / 1000

    # EVENTS

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    # RENDERING

    game_surface.blit(background_image, (0, 0))
    game_surface.blit(ground_image, (0, VIRTUAL_HEIGHT - ground_image.get_height()))

    # Scale the game surface to fit the window
    scale, scaled_xy, offset = compute_letterbox(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, screen)
    scaled = pg.transform.scale(game_surface, scaled_xy)
    screen.blit(scaled, offset)

    pg.display.flip()

