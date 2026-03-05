import pygame as pg


# Settings -----------------------------------------

## Display

FPS = 60
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
VIRTUAL_WIDTH = 432
VIRTUAL_HEIGHT = 243

## Colours

WHITE = (255, 255, 255)
GREY = (40, 52, 55, 255)

BACKGROUND_COLOUR = GREY


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

## Game variables

player1_score = 0
player2_score = 0

player1_y = 30
player2_y = VIRTUAL_HEIGHT - 50

PADDLE_SPEED = 200


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

    keys = pg.key.get_pressed()
    
    if keys[pg.K_s]:
        player1_y += PADDLE_SPEED * dt
    if keys[pg.K_w]:
        player1_y -= PADDLE_SPEED * dt
    if keys[pg.K_DOWN]:
        player2_y += PADDLE_SPEED * dt
    if keys[pg.K_UP]:
        player2_y -= PADDLE_SPEED * dt

    # Rendering
    game_surface.fill(BACKGROUND_COLOUR)

    ## Paddles
    pg.draw.rect(game_surface, WHITE, (10, player1_y, 5, 20))
    pg.draw.rect(game_surface, WHITE, (VIRTUAL_WIDTH - 10, player2_y, 5, 20))
    
    ## Ball
    pg.draw.rect(game_surface, WHITE, (VIRTUAL_WIDTH // 2 - 2, VIRTUAL_HEIGHT // 2 - 2, 4, 4))

    ## Title
    text = SMALL_FONT.render("Hello Pong!", False, WHITE)
    game_surface.blit(text, (VIRTUAL_WIDTH // 2 - text.get_width() // 2, 0))

    ## Score
    score1 = SCORE_FONT.render(str(player1_score), False, WHITE)
    score2 = SCORE_FONT.render(str(player2_score), False, WHITE)
    game_surface.blit(score1, (VIRTUAL_WIDTH // 2 - 50, VIRTUAL_HEIGHT // 3))
    game_surface.blit(score2, (VIRTUAL_WIDTH // 2 + 30, VIRTUAL_HEIGHT // 3))

    # Scale the game surface to fit the window
    scaled = pg.transform.scale(game_surface, screen.get_size())
    screen.blit(scaled, (0, 0))

    pg.display.flip()

pg.quit()