import pygame as pg
import random

from Ball import Ball
from Paddle import Paddle
from settings import *


# Initialize Pygame -----------------------------------------

pg.init()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_surface = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
clock = pg.time.Clock()
running = True

## Fonts

FONT = pg.font.Font("font.ttf", 36)
SMALL_FONT = pg.font.Font("font.ttf", 8)
SCORE_FONT = pg.font.Font("font.ttf", 32)

## Game classes

player1_score = 0
player2_score = 0

player1 = Paddle(PADDLE_MARGIN_X, PADDLE_MARGIN_Y)
player2 = Paddle(
    VIRTUAL_WIDTH - PADDLE_MARGIN_X - PADDLE_WIDTH,
    VIRTUAL_HEIGHT - PADDLE_MARGIN_Y - PADDLE_HEIGHT
)
ball = Ball(
    VIRTUAL_WIDTH // 2 - BALL_SIZE // 2,
    VIRTUAL_HEIGHT // 2 - BALL_SIZE // 2
)

game_state = "start"


## Functions

def display_FPS(surface):
    fps = int(clock.get_fps())
    text = SMALL_FONT.render(f"FPS: {fps}", False, WHITE)
    surface.blit(text, (10, 10))


# Main game loop -----------------------------------------

while running:

    # Cap the frame rate
    dt = clock.tick(FPS) / 1000

    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

            if event.key == pg.K_RETURN:
                if game_state == "start":
                    game_state = "play"

    keys = pg.key.get_pressed()

    if game_state == "play":
        if keys[pg.K_s]:
            player1.update(1, dt)
        if keys[pg.K_w]:
            player1.update(-1, dt)
        if keys[pg.K_DOWN]:
            player2.update(1, dt)
        if keys[pg.K_UP]:
            player2.update(-1, dt)

        ball.update(dt)

    # Rendering
    game_surface.fill(BACKGROUND_COLOUR)

    ## Paddles
    player1.render(game_surface)
    player2.render(game_surface)

    ## Ball
    ball.render(game_surface)

    ## Title
    text = SMALL_FONT.render("Hello Pong!", False, WHITE)
    game_surface.blit(text, (VIRTUAL_WIDTH // 2 - text.get_width() // 2, 0))

    ## Score
    score1 = SCORE_FONT.render(str(player1_score), False, WHITE)
    score2 = SCORE_FONT.render(str(player2_score), False, WHITE)
    game_surface.blit(score1, (VIRTUAL_WIDTH // 2 - 50, VIRTUAL_HEIGHT // 3))
    game_surface.blit(score2, (VIRTUAL_WIDTH // 2 + 30, VIRTUAL_HEIGHT // 3))

    # FPS
    display_FPS(game_surface)

    # Scale the game surface to fit the window
    scaled = pg.transform.scale(game_surface, screen.get_size())
    screen.blit(scaled, (0, 0))

    pg.display.flip()

pg.quit()