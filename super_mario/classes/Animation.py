import math

import pygame as pg

class Animation:

    def __init__(self, frames, interval):

        self.frames = frames
        self.interval = interval
        self.timer = 0
        self.current_frame = 0


    def update(self, dt):
        
        # animations with 0 or 1 frames need no animation
        if len(self.frames) <= 1:
            return
        
        self.timer += dt

        if self.timer > self.interval:
            self.timer = self.timer % self.interval

            self.current_frame = math.max(1, (self.current_frame + 1) % (len(self.frames + 1)))

    
    def get_current_frame(self):
        return self.frames[self.current_frame]