import pygame as pg    

from match3.src.settings import TILE_SIZE


class Tile:

    def __init__(self, x, y, asset_manager, colour, variety=0):
        
        # board position
        self.col = x
        self.row = y

        # surface and rect
        self.surf = asset_manager.images["tiles"][colour][variety]
        self.rect = self.surf.get_frect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

        # tile properties
        self.colour = colour
        self.variety = variety

        # tweening properties
        self.tweening = False
        self.tween_elapsed_time = 0
        self.tween_duration = 0.6 #s
        self.tween_start_pos = (0, 0)
        self.tween_target_pos = (0, 0)


    def __repr__(self):
        return f"Tile(col={self.col}, row={self.row}, colour={self.colour}, variety={self.variety})"


    def start_tween(self, target_pos):
        self.tweening = True
        self.tween_elapsed_time = 0
        self.tween_start_pos = self.rect.topleft
        self.tween_target_pos = target_pos


    def update(self, dt):
        self.rect.topleft = (self.col * TILE_SIZE, self.row * TILE_SIZE)

        if not self.tweening:
            return
        
        self.tween_elapsed_time += dt
        if self.tween_elapsed_time >= self.tween_duration:
            self.tweening = False
            self.rect.topleft = self.tween_target_pos
        else:
            t = self.tween_elapsed_time / self.tween_duration
            new_x = self.tween_start_pos[0] + (self.tween_target_pos[0] - self.tween_start_pos[0]) * t
            new_y = self.tween_start_pos[1] + (self.tween_target_pos[1] - self.tween_start_pos[1]) * t
            self.rect.topleft = (new_x, new_y)



    def render(self, surface, offset):

        render_x = self.rect.x + offset[0]
        render_y = self.rect.y + offset[1]
        surface.blit(self.surf, (render_x, render_y))



