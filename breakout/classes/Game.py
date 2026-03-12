import pygame as pg

from breakout.assets.assets import Assets
from breakout.classes.states.StartState import StartState
from breakout.classes.StateMachine import StateMachine
from breakout.src.settings import FPS, VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from breakout.src.utils import compute_letterbox, display_fps

class Game:
    def __init__(self):
        
        pg.init()

        self.display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.RESIZABLE)
        pg.display.set_caption("Breakout")

        self.game_surface = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

        # Assets

        self.assets = Assets()
        self.assets.load_assets("breakout/assets/")

        # State machine

        self.state_engine = StateMachine()
        self.state_engine.game = self
        self.state_engine.add_state("start", StartState())
        self.state_engine.change_state("start")

        self.events = None
        self.keys_pressed = None

        # Debug

        self.debug = True

        # Game elements

        self.background = self.assets.get_image("background")
        self.background = pg.transform.scale(self.background, (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

        self.running = True
        self.clock = pg.time.Clock()
        self.dt = 0

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update()
            self.render()

        pg.quit()

    def handle_events(self):
        self.keys_pressed = pg.key.get_pressed()
        self.events = []

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                self.events.append(event)

    def update(self):

        self.state_engine.update()

    def render(self):

        # Background

        self.game_surface.blit(self.background, (0, 0))
        
        # Render state
        
        self.state_engine.render(self.game_surface)

        # Debug

        if self.debug:
            display_fps(self.clock, self.game_surface)

        # Letterbox the display
        scale, scale_w_h, offset = compute_letterbox(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, self.display)
        scaled_letterbox = pg.transform.scale(self.game_surface, scale_w_h)
        self.display.blit(scaled_letterbox, offset)

        pg.display.flip()