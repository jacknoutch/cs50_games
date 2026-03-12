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


def generate_quads(sheet, quad_width, quad_height):
    """
    Generate a list of quads (rectangles) from the given sprite sheet.
    """
    quads = []
    sheet_width, sheet_height = sheet.get_size()
    for y in range(0, sheet_height, quad_height):
        for x in range(0, sheet_width, quad_width):
            quads.append((x, y, quad_width, quad_height))
    return quads


def generate_paddles(sheet) -> dict:
    """
    Generate paddle sprites from the given sprite sheet.

    Returns a dictionary mapping colours, sizes, and paddle surfaces.
    """
    print(sheet.get_size())
    colours = ["blue", "green", "red", "purple"]

    paddles = {colour: {} for colour in colours}

    # blocks.png paddles begin at 64, 0
    x = 0
    y = 64

    # paddle dimensions
    paddle_height = 16
    small_paddle_width = 32
    medium_paddle_width = 64
    large_paddle_width = 96
    huge_paddle_width = 128

    for i, colour in enumerate(paddles.keys()):
        print(f"Generating paddles for {colour}")

        # print(f"  Small paddle: x: {x}, y: {y + i * paddle_height * 2}")
        small_paddle = sheet.subsurface(x, y + i * paddle_height * 2,
                                        small_paddle_width, paddle_height)
        
        # print(f"  Medium paddle: x: {x + small_paddle_width}, y: {y + i * paddle_height * 2}")
        medium_paddle = sheet.subsurface(x + small_paddle_width, y + i * paddle_height * 2,
                                         medium_paddle_width, paddle_height)
        
        # print(f"  Large paddle: x: {x + small_paddle_width + medium_paddle_width}, y: {y + i * paddle_height * 2}")
        large_paddle = sheet.subsurface(x + small_paddle_width + medium_paddle_width, y + i * paddle_height * 2,
                                        large_paddle_width, paddle_height)

        # print(f"  Huge paddle: x: {x}, y: {y + paddle_height * (2 * i + 1)}")
        huge_paddle = sheet.subsurface(x, y + paddle_height * (2 * i + 1), 
                                       huge_paddle_width, paddle_height)

        paddles[colour] = {
            "small": small_paddle,
            "medium": medium_paddle,
            "large": large_paddle,
            "huge": huge_paddle
        }

    return paddles