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


# Initialize Pygame -----------------------------------------

pg.init()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_surface = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
clock = pg.time.Clock()
running = True

## Fonts

FONT = pg.font.Font(None, 36)


# Main game loop -----------------------------------------

while running:

    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    # Rendering
    game_surface.fill((0, 0, 0))

    text = FONT.render("Hello Pong!", False, WHITE)
    game_surface.blit(text, (VIRTUAL_WIDTH // 2 - text.get_width() // 2, VIRTUAL_HEIGHT // 2 - text.get_height() // 2))

    # Scale the game surface to fit the window
    scaled = pg.transform.scale(game_surface, screen.get_size())
    screen.blit(scaled, (0, 0))

    pg.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pg.quit()