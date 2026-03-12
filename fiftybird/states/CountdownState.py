import pygame as pg

from fiftybird.assets import assets
from fiftybird.settings import VIRTUAL_WIDTH, VIRTUAL_HEIGHT
from fiftybird.states.BaseState import BaseState

COUNTDOWNTIME = 0.75 # Time in seconds for each countdown tick'

class CountdownState(BaseState):
    def __init__(self):
        super().__init__()
        self.timer = 0
        self.count = 3

    def update(self, dt: float, keys_pressed: pg.key.ScancodeWrapper):
        self.timer += dt

        if self.timer > COUNTDOWNTIME:
            self.timer = self.timer % COUNTDOWNTIME
            self.count -= 1

            if self.count == 0:
                self.state_machine.change_state("play")

    def render(self, surface: pg.Surface):
        text = assets.huge_font.render(f"{self.count:.0f}", False, (255, 255, 255))
        surface.blit(text, (VIRTUAL_WIDTH // 2 - text.get_width() // 2, VIRTUAL_HEIGHT // 2 - text.get_height() // 2))