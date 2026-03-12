import pygame as pg

from wk1.settings import VIRTUAL_WIDTH
from wk1.assets import assets
from wk1.states.BaseState import BaseState


class ScoreState(BaseState):
    def __init__(self, score: int):
        super().__init__()
        self.score = score

    def update(self, dt: float, keys_pressed: pg.key.ScancodeWrapper):

        if keys_pressed[pg.K_RETURN]:
            self.state_machine.change_state('play')

    def render(self, surface: pg.Surface):

        # Render the "Game Over" text to the center of the screen
        text = assets.flappy_font.render(f"Oof! You lost!", False, (255, 255, 255))
        surface.blit(text, (VIRTUAL_WIDTH // 2 - text.get_width() // 2, 64))

        text = assets.flappy_font.render(f"Score: {self.score}", False, (255, 255, 255))
        surface.blit(text, (VIRTUAL_WIDTH // 2 - text.get_width() // 2, 128))

        text = assets.flappy_font.render(f"Press Enter to play again!", False, (255, 255, 255))
        surface.blit(text, (VIRTUAL_WIDTH // 2 - text.get_width() // 2, 192))