import pygame as pg
import random

from wk1.Bird import Bird
from wk1.Pipe import Pipe
from wk1.PipePair import PipePair
from wk1.StateMachine import StateMachine
from wk1.settings import *
from wk1.states import PlayState, TitleScreenState
from wk1.utils import compute_letterbox

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

scrolling = True

## State Machine

state_machine = StateMachine({
    "play": PlayState.PlayState(),
    "title": TitleScreenState.TitleScreenState()
})

state_machine.change_state("play")

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

    # LOGIC

    if scrolling:

        keys_pressed = pg.key.get_just_pressed()

        background_scroll = (background_scroll + BACKGROUND_SCROLL_SPEED * dt) % BACKGROUND_LOOPING_X
        ground_scroll = (ground_scroll + GROUND_SCROLL_SPEED * dt) % VIRTUAL_WIDTH

        state_machine.update(dt, keys_pressed)

    # RENDERING

    game_surface.blit(background_image, (-background_scroll, 0))
    game_surface.blit(ground_image, (-ground_scroll, VIRTUAL_HEIGHT - ground_image.get_height()))
    state_machine.render(game_surface)

    # Scale the game surface to fit the window
    scale, scaled_xy, offset = compute_letterbox(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, screen)
    scaled = pg.transform.scale(game_surface, scaled_xy)
    screen.blit(scaled, offset)

    pg.display.flip()

