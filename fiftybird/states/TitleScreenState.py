import pygame as pg

from wk0.settings import WHITE
from fiftybird.assets import assets
from fiftybird.settings import VIRTUAL_WIDTH
from fiftybird.states.BaseState import BaseState


class TitleScreenState(BaseState):
    def __init__(self,):
        super().__init__()

    def update(self, dt: float, keys_pressed: pg.key.ScancodeWrapper):
        
        if keys_pressed[pg.K_RETURN]:
            self.state_machine.change_state("countdown")

    def render(self, surface):

        title = assets.flappy_font.render(f"Fifty Bird", False, WHITE)
        instructions = assets.medium_font.render("Press Enter", False, WHITE)
        surface.blit(title, (VIRTUAL_WIDTH // 2 - title.get_width() // 2, 0))
        surface.blit(instructions, (VIRTUAL_WIDTH // 2 - instructions.get_width() // 2, 36))
