import pygame as pg

# Initialize Pygame
pg.init()
screen = pg.display.set_mode((1280, 720))
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
    pg.display.flip()

    # Cap the frame rate
    clock.tick(60)

pg.quit()