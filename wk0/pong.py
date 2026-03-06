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

serving_player = 1

winning_player = None


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
                    game_state = "serve"
                elif game_state == "serve":
                    game_state = "play"
                elif game_state == "done":
                    game_state = "serve"
                    ball.reset()
                    player1_score = 0
                    player2_score = 0
                    if winning_player == 1:
                        serving_player = 2
                    elif winning_player == 2:
                        serving_player = 1

    keys = pg.key.get_pressed()

    if game_state == "serve":
        ball.dy = random.randint(-50, 50)
        if serving_player == 1:
            ball.dx = random.randint(140,200)
        elif serving_player == 2:
            ball.dx = -random.randint(140,200)

    elif game_state == "play":
        if keys[pg.K_s]:
            player1.update(1, dt)
        if keys[pg.K_w]:
            player1.update(-1, dt)
        if keys[pg.K_DOWN]:
            player2.update(1, dt)
        if keys[pg.K_UP]:
            player2.update(-1, dt)

        ball.update(dt)

    ## Ball collision

    if ball.collides(player1):
        ball.dx *= -1.03
        ball.x = player1.x + player1.width

        if ball.dy < 0:
            ball.dy = -random.randint(10, 150)
        else:
            ball.dy = random.randint(10, 150)

    elif ball.collides(player2):
        ball.dx *= -1.03
        ball.x = player2.x - ball.width

        if ball.dy < 0:
            ball.dy = -random.randint(10, 150)
        else:
            ball.dy = random.randint(10, 150)

    if ball.y <= 0:
        ball.y = 0
        ball.dy *= -1

    elif ball.y >= VIRTUAL_HEIGHT - ball.height:
        ball.y = VIRTUAL_HEIGHT - ball.height
        ball.dy *= -1

    ## Scoring and winning

    if ball.x <= 0 and game_state == "play":
        serving_player = 1
        player2_score += 1

        if player2_score >= WINNING_SCORE:
            winning_player = 2
            game_state = "done"
        else:
            ball.reset()
            game_state = "serve"

    elif ball.x >= VIRTUAL_WIDTH - ball.width and game_state == "play":
        serving_player = 2
        player1_score += 1

        if player1_score >= WINNING_SCORE:
            winning_player = 1
            game_state = "done"
        else:
            ball.reset()
            game_state = "serve"


    # Rendering
    game_surface.fill(BACKGROUND_COLOUR)

    ## Paddles
    player1.render(game_surface)
    player2.render(game_surface)

    ## Ball
    ball.render(game_surface)

    if game_state == "start":
        text1 = SMALL_FONT.render("Welcome to Pong!", False, WHITE)
        text2 = SMALL_FONT.render("Press Enter to begin", False, WHITE)
        game_surface.blit(text1, (VIRTUAL_WIDTH // 2 - text1.get_width() // 2, 0))
        game_surface.blit(text2, (VIRTUAL_WIDTH // 2 - text2.get_width() // 2, 20))

    elif game_state == "serve":
        text1 = SMALL_FONT.render(f"Player {serving_player}'s serve", False, WHITE)
        text2 = SMALL_FONT.render("Press Enter to serve", False, WHITE)
        game_surface.blit(text1, (VIRTUAL_WIDTH // 2 - text1.get_width() // 2, 0))
        game_surface.blit(text2, (VIRTUAL_WIDTH // 2 - text2.get_width() // 2, 20))

    elif game_state == "done":
        text1 = SMALL_FONT.render(f"Player {winning_player} wins!", False, WHITE)
        text2 = SMALL_FONT.render("Press Enter to restart", False, WHITE)
        game_surface.blit(text1, (VIRTUAL_WIDTH // 2 - text1.get_width() // 2, 0))
        game_surface.blit(text2, (VIRTUAL_WIDTH // 2 - text2.get_width() // 2, 20))

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