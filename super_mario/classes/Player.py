import pygame as pg

from super_mario.classes.Animation import Animation
from super_mario.src.settings import TILE_SIZE

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

        self.current_frame = 0

        self.idle_animation = Animation(self.frames[0], interval=1)
        self.moving_animation = Animation(self.frames[10, 11], interval=0.2)

        self.current_animation = self.idle_animation

        

        self.rect = self.get_surf().get_rect()
        self.x = self.rect.x
        self.y = self.rect.y

        self.speed = 160


        # 

        self.tile_x = 7
        self.tile_y = 4


    def update(self):

        # POSITION

        self.rect = self.get_surf().get_rect(topleft=self.rect.topleft)

    
    def render(self, surface):

        pos = (self.tile_x * TILE_SIZE, self.tile_y* TILE_SIZE + TILE_SIZE - self.tile_height)

        surface.blit(self.frames[self.current_frame], pos)

    #----------

    def get_surf(self):
        return self.frames[self.current_frame]

    def move(self, dx):

        self.rect.x += dx * self.speed