import os
import pygame as pg

from match3.classes.states.StartState import StartState
from match3.assets.AssetManager import AssetManager
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

        self.asset_manager = AssetManager()
        self.asset_manager.load_assets()

        # DEBUG

        self.debug = True

        # STATE MACHINE

        self.state_machine = StateMachine()
        self.state_machine.game = self
        self.state_machine.add_state("start", StartState())
        self.state_machine.change_state("start")

        self.events = None
        self.keys_pressed = None
        self.mouse_pressed = None

        # GAME ELEMENTS

        self.clock = pg.time.Clock()
        self.dt = 0

        self.background = self.asset_manager.get_image("background")
        self.background = pg.transform.scale2x(self.background)

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

            self.events.append(event)

            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

                if event.key == pg.K_d:
                    self.debug = not self.debug


    def update(self):
        
        self.state_machine.update(self.dt)
        

    def render(self):

        self.game_surface.blit(self.background, (0, 0))

        self.state_machine.render(self.game_surface)

        if self.debug:
            display_fps(self.clock, self.game_surface)

        # letterbox the display
        scale, scale_w_h, offset = compute_letterbox(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, self.display)
        scaled_letterbox = pg.transform.scale(self.game_surface, scale_w_h)
        self.display.blit(scaled_letterbox, offset)

        pg.display.flip()
