import os
import pygame as pg

from match3.classes.StateMachine import StateMachine
from match3.src.settings import FPS, VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from match3.src.utils import compute_letterbox, display_fps, debug

class Game:


    def __init__(self):
        
        pg.init()
        
        # DISPLAY

        self.display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.game_surface = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        pg.display.set_caption("Match 3")

        # ASSETS

        # STATE MACHINE

        self.state_machine = StateMachine()
        self.state_machine.game = self

        self.events = None
        self.keys_pressed = None
        self.mouse_pressed = None

        # DEBUG

        self.debug = True

        # GAME ELEMENTS

        self.clock = pg.time.Clock()
        self.dt = 0

        self.running = True


    def run(self):

        while self.running:

            self.dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update()
            self.render()

        pg.quit()
        os.sys.exit()


    def handle_events(self):
            
        self.keys_pressed = pg.key.get_pressed()
        self.events = []

        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                self.events.append(event)
    
                if event.key == pg.K_ESCAPE:
                    self.running = False

                if event.key == pg.K_d:
                    self.debug = not self.debug


    def update(self):
        
        self.state_machine.update(self.dt)
        

    def render(self):

        # background
        self.game_surface.fill((40, 40, 40))

        self.state_machine.render(self.game_surface)

        if self.debug:
            display_fps(self.clock, self.game_surface)

        # letterbox the display
        scale, scale_w_h, offset = compute_letterbox(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, self.display)
        scaled_letterbox = pg.transform.scale(self.game_surface, scale_w_h)
        self.display.blit(scaled_letterbox, offset)

        pg.display.flip()
