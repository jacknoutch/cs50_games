import pygame as pg
import random

from breakout.classes.Brick import Brick
from breakout.classes.Paddle import Paddle
from breakout.src.settings import VIRTUAL_HEIGHT, VIRTUAL_WIDTH

BALL_WIDTH = 8
BALL_HEIGHT = 8
BALL_SPEED = 120
BALL_COLLISION_MARGIN = -2

class Ball:
    def __init__(self, surface, sounds: dict):
        self.width = BALL_WIDTH
        self.height = BALL_HEIGHT
        self.colour = None
        self.surf = surface
        self.rect = self.surf.get_frect()
        self.sounds = sounds

        self.last_collided = None
        self.speed = BALL_SPEED
        self.direction = pg.Vector2(0, 0)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction.x *= random.uniform(-0.9, -1.1)  # Add some randomness to the bounce
            self.direction = self.direction.normalize()
            self.sounds["wall_hit"].play()
        elif self.rect.right >= VIRTUAL_WIDTH:
            self.rect.right = VIRTUAL_WIDTH
            self.direction.x *= random.uniform(-0.9, -1.1)  # Add some randomness to the bounce
            self.direction = self.direction.normalize()
            self.sounds["wall_hit"].play()
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= random.uniform(-0.9, -1.1)  # Add some randomness to the bounce
            self.direction = self.direction.normalize()
            self.sounds["wall_hit"].play()
        elif self.rect.bottom >= VIRTUAL_HEIGHT:
            self.rect.bottom = VIRTUAL_HEIGHT
            self.direction.y *= random.uniform(-0.9, -1.1)  # Add some randomness to the bounce
            self.direction = self.direction.normalize()
            self.sounds["wall_hit"].play()

    def render(self, surface):
        surface.blit(self.surf, self.rect)

    def collide(self, other, dt=None):
        """
        Check for collision with another object and return the overlap shift vector.
        """
        a = other.rect  # platform rect
        b = self.rect   # ball rect

        # Calculate overlap on each axis
        overlap_x = min(a.right, b.right) - max(a.left, b.left)
        overlap_y = min(a.bottom, b.bottom) - max(a.top, b.top)

        if overlap_x > 0 and overlap_y > 0:
            
            # If we're still overlapping the same object we last bounced off,
            # don't bounce again — just keep correcting position
            if self.last_collided == other:
                return False

            # Use direction direction to determine correct shift direction
            shift_x = overlap_x if self.direction.x > 0 else -overlap_x
            shift_y = overlap_y if self.direction.y > 0 else -overlap_y

            # If colliding with a moving Paddle, add the paddle's movement to the shift
            if dt is not None and isinstance(other, Paddle):
                paddle_dx = other.direction.x * other.speed * dt
                shift_x += paddle_dx

            shift_ball = pg.math.Vector2(shift_x, shift_y)
            return shift_ball
        
        # Ball has left the object, clear the lock
        if self.last_collided == other:
            self.last_collided = None

        return False

    def bounce(self, shift_ball: pg.math.Vector2, other):

        # Resolve along the axis with the smallest overlap (most likely entry side)
        if abs(shift_ball.x) < abs(shift_ball.y):
            self.rect.centerx -= shift_ball.x  # push ball out horizontally
            self.direction.x *= -1
        else:
            self.rect.centery -= shift_ball.y  # push ball out vertically
            self.direction.y *= -1

        if isinstance(other, Paddle):
            self.direction.x += other.direction.x  # Add some of the paddle's horizontal movement to the ball
            self.direction = self.direction.normalize()  # Normalize to maintain speed
            self.speed *= 1.02
            self.sounds["paddle_hit"].play()
        elif isinstance(other, Brick):  # Assuming bricks are sprites
            self.sounds["brick-hit-2"].play()

    def reset(self):
        self.rect.center = (VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2)
        self.direction = pg.Vector2(0, 0)

    def start(self):
        """
        Set the ball in motion at a random angle upwards.
        """
        x = random.uniform(-1, 1)
        y = random.uniform(-1, -0.5)
        self.direction = pg.Vector2(x, y)