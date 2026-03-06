import pygame as pg
import random

from Bird import Bird
from Pipe import Pipe
from PipePair import PipePair
from settings import *
from utils import compute_letterbox

# INITIALISATION

pg.init()

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.RESIZABLE)

pg.display.set_caption("Fifty Bird")

game_surface = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

clock = pg.time.Clock()

## Images

background_image = pg.image.load(BACKGROUND_IMAGE).convert()
ground_image = pg.image.load(GROUND_IMAGE).convert()

background_scroll = 0
ground_scroll = 0

## Game objects

bird = Bird()

spawn_timer = 0

previous_pipe_y = -PIPE_HEIGHT + random.randint(0, 80) + 20

pipe_pairs = [
    pipe_pair := PipePair(y=previous_pipe_y),
]

running = True

while running:

    dt = clock.tick(FPS) / 1000
    spawn_timer += dt

    # EVENTS

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    # LOGIC

    keys_pressed = pg.key.get_just_pressed()

    bird.update(dt, keys_pressed)

    if spawn_timer >= PIPE_SPAWN_INTERVAL:
        y = max(-PIPE_HEIGHT + 10, min(previous_pipe_y + random.randint(-20, 20), VIRTUAL_HEIGHT - PIPE_HEIGHT - PIPE_GAP))
        previous_pipe_y = y
        pipe_pairs.append(PipePair(y=y))
        spawn_timer = 0

    for pipe_pair in pipe_pairs[:]:
        pipe_pair.update(dt)

        if pipe_pair.remove:
            pipe_pairs.remove(pipe_pair)

    background_scroll = (background_scroll + BACKGROUND_SCROLL_SPEED * dt) % BACKGROUND_LOOPING_X
    ground_scroll = (ground_scroll + GROUND_SCROLL_SPEED * dt) % VIRTUAL_WIDTH

    # RENDERING

    game_surface.blit(background_image, (-background_scroll, 0))
    game_surface.blit(ground_image, (-ground_scroll, VIRTUAL_HEIGHT - ground_image.get_height()))

    bird.render(game_surface)

    for pipe_pair in pipe_pairs:
        pipe_pair.render(game_surface)

    # Scale the game surface to fit the window
    scale, scaled_xy, offset = compute_letterbox(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, screen)
    scaled = pg.transform.scale(game_surface, scaled_xy)
    screen.blit(scaled, offset)

    pg.display.flip()

