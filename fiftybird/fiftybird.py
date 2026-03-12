import pygame as pg
import random

from fiftybird.assets import assets
from fiftybird.StateMachine import StateMachine
from fiftybird.settings import *
from fiftybird.states import CountdownState, PlayState, ScoreState, TitleScreenState
from fiftybird.utils import compute_letterbox

# INITIALISATION

pg.init()

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.RESIZABLE)

pg.display.set_caption("Fifty Bird")

game_surface = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

clock = pg.time.Clock()

## Images

assets.load_assets()  # load assets after display is initialized

background_image = assets.background
ground_image = assets.ground

background_scroll = 0
ground_scroll = 0

## Music (loop)

assets.main_music.play(-1)

## State Machine

state_machine = StateMachine({
    "countdown": CountdownState.CountdownState,
    "play": PlayState.PlayState,
    "score": ScoreState.ScoreState,
    "title": TitleScreenState.TitleScreenState
})

state_machine.change_state("title")

keys_pressed = pg.key.ScancodeWrapper()

running = True

## Debug

def debug(info, y=10, x=10):
    text = assets.small_font.render(str(info), False, (255, 255, 255))
    surf = pg.Surface((text.get_width() + 4, text.get_height() + 4))
    surf.fill((0, 0, 0))
    surf.blit(text, (2, 2))
    game_surface.blit(surf, (x, y))


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

