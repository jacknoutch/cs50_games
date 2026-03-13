import pygame as pg

from breakout.classes.Brick import BRICK_COLOURS

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


def generate_balls(sheet) -> dict:
    """
    Generate ball sprites from the given sprite sheet.

    Returns a dictionary mapping ball colours to their surfaces.
    """
    print(sheet.get_size())
    
    x = 32 * 3
    y = 16 * 3

    ball_width = 8
    ball_height = 8

    row_length = 4
    colours = ["blue", "green", "red", "purple", "yellow", "grey", "gold"]

    balls = {}

    for i, colour in enumerate(colours):
        # print(f"Generating ball sprite for {colour}")
        # print(f"  Position: ({x + i * ball_width % row_length}, {y + i // row_length * ball_height})")
        ball = sheet.subsurface(
            x + i * ball_width % row_length,
            y + i // row_length * ball_height,
            ball_width, ball_height
            )
        balls[colour] = ball

    return balls


def generate_bricks(sheet) -> dict:
    """
    Generate brick sprites from the given sprite sheet.

    Returns a dictionary mapping brick colours to their surfaces.
    """
    print(sheet.get_size())

    x = 0
    y = 0

    brick_width = 32
    brick_height = 16
    row_length = 6

    colours = BRICK_COLOURS
    tiers = 4

    bricks = {}

    for i, colour in enumerate(colours):
        bricks[colour] = []
        for j in range(tiers):
            print(f"Generating brick sprite for {colour} - {j}")
            print(f"  Position: ({x + ((i * tiers + j) * brick_width) % (row_length * brick_width)}, {y + (i * tiers + j) // 6 * brick_height})")
            brick = sheet.subsurface(
                x + ((i * tiers + j) * brick_width) % (row_length * brick_width),
                y + (i * tiers + j) // 6 * brick_height,
                brick_width, brick_height
            )
            bricks[colour].append(brick)

    return bricks


def generate_hearts(sheet) -> dict:
    """
    Generate heart sprites from the given sprite sheet.

    Returns a dictionary mapping heart statuses to their surfaces.
    """
    print(sheet.get_size())

    x = 0
    y = 0

    heart_width = 10
    heart_height = 9

    hearts = {
        "full": sheet.subsurface(x, y, heart_width, heart_height),
        "empty": sheet.subsurface(x + heart_width, y, heart_width, heart_height)
    }

    return hearts


def debug(info, surface, x, y):
    # Display debug information
    font = pg.font.Font(None, 12)
    text = font.render(info, False, (255, 255, 255))
    background = pg.Surface(text.get_size())
    background.fill((0, 0, 0))
    background.blit(text, (0, 0))
    surface.blit(background, (x, y))