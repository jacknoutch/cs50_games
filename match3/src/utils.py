import pygame as pg

def compute_letterbox(virtual_width, virtual_height, window):
    """
    Compute scale and centered rectangle to render a virtual surface into a window
    while preserving aspect ratio (letterbox/pillarbox).

    Returns (scale, (scaled_width, scaled_height), (offset_x, offset_y)).
    """
    window_width, window_height = window.get_size()

    if virtual_width <= 0 or virtual_height <= 0 or window_width <= 0 or window_height <= 0:
        return 0, (0, 0), (0, 0)

    scale = min(window_width / virtual_width, window_height / virtual_height)
    scaled_width = int(virtual_width * scale)
    scaled_height = int(virtual_height * scale)
    offset_x = (window_width - scaled_width) // 2
    offset_y = (window_height - scaled_height) // 2

    return scale, (scaled_width, scaled_height), (offset_x, offset_y)

def display_fps(clock, surface):
    """
    Display the current frames per second (FPS) in the top left corner of the given surface.
    """
    text = pg.font.SysFont(None, 14).render(f"FPS: {int(clock.get_fps())}", False, (255, 255, 255))
    surf = pg.Surface(text.get_size())
    surf.fill((0, 0, 0))
    surf.blit(text, (0, 0))
    surface.blit(surf, (1, 1))

def debug(info, surface, x, y):
    """
    Display debug information on the given surface at the specified position.
    """
    font = pg.font.Font(None, 12)
    text = font.render(info, False, (255, 255, 255))
    background = pg.Surface(text.get_size())
    background.fill((0, 0, 0))
    background.blit(text, (0, 0))
    surface.blit(background, (x, y))