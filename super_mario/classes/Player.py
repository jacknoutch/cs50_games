import pygame as pg

from super_mario.classes.Animation import Animation
from super_mario.src.settings import GRAVITY, JUMP_VELOCITY, TILE_SIZE

class Player:

    def __init__(self):

        path = "super_mario/assets/character.png"

        sheet = pg.image.load(path).convert_alpha()
        self.tile_height = 20
        self.tile_width = 16

        self.frames_count = 11
        self.frames = []

        for x in range(self.frames_count):
            rect = pg.Rect(x * self.tile_width, 0, self.tile_width, self.tile_height)
            frame = sheet.subsurface(rect).copy()
            self.frames.append(frame)

        self.idle_animation = Animation([self.frames[0]], interval=1)
        self.moving_animation = Animation(self.frames[9:11], interval=0.2)
        self.jump_animation = Animation([self.frames[2]], interval=0.2)
        self.current_animation = self.idle_animation
        

        self.speed = 80
        self.dy = 0
        self.direction = "right"
        self.movement_state = "idle"
        self.on_ground = True
        self.moving = False


        self.start_tile_x = 7
        self.start_tile_y = 4
        
        self.frect = self.get_surf().get_rect()
        self.x = float(self.start_tile_x * TILE_SIZE)
        self.y = float(self.start_tile_y * TILE_SIZE + TILE_SIZE - self.tile_height)
        self.frect.topleft = (int(self.x), int(self.y))


    def update(self, dt):

        # up and down
        self.dy += GRAVITY * dt
        self.y += self.dy * dt

        # clamp to ground
        ground_y = ((6 - 1) * TILE_SIZE) - self.frect.height
        self.on_ground = False
        if self.y > ground_y:
            self.y = ground_y
            self.frect.y = int(self.y)
            self.dy = 0
            self.on_ground = True

        if not self.on_ground:
            self.movement_state = "jumping"
        elif self.moving:
            self.movement_state = "moving"
        else:
            self.movement_state = "idle"

        if self.movement_state == "jumping":
            self.current_animation = self.jump_animation
        elif self.movement_state == "moving":
            self.current_animation = self.moving_animation
        else:
            self.current_animation = self.idle_animation

        self.current_animation.update(dt)

        self.frect = self.get_surf().get_rect(topleft=(int(self.x), int(self.y)))

        self.moving = False
        

    
    def render(self, surface):

        surface.blit(self.get_surf(), (self.frect.x, self.frect.y))


    #----------


    def get_surf(self):
        surf = self.current_animation.get_current_frame()
        if self.direction == "left":
            return pg.transform.flip(surf, True, False)
        return surf


    def move(self, dx):

        self.x += dx * self.speed
        self.frect.x = int(self.x)
        self.moving = True
        self.direction = "left" if dx < 0 else "right"

    
    def jump(self):
        self.dy = JUMP_VELOCITY