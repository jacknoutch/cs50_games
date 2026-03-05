import pygame as pg

# Settings
FPS = 60
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WHITE = (255, 255, 255)


# Initialize Pygame
pg.init()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pg.time.Clock()
running = True


# Main game loop
while running:

    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Rendering
    screen.fill((0, 0, 0))

    font = pg.font.Font(None, 36)
    text = font.render("Hello Pong!", True, WHITE)
    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))

    pg.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pg.quit()