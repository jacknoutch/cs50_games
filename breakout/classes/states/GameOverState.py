import pygame as pg

from breakout.classes.states.BaseState import BaseState
from breakout.src.settings import MAX_HEALTH, VIRTUAL_HEIGHT, VIRTUAL_WIDTH

class GameOverState(BaseState):
    def __init__(self):
        super().__init__()
        self.score = 0

    def enter(self):
        print("Entering Game Over State")

        self.score = self.state_machine.game.score
        self.fonts = self.state_machine.game.assets.fonts
        self.state_machine.game.health = MAX_HEALTH

    def exit(self):
        print("Exiting Game Over State")

    def update(self, dt):
        events = self.state_machine.game.events

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.state_machine.change_state("start")

    def render(self, surface):
        font = self.fonts["large_font"]
        text = font.render("Game Over", False, (255, 0, 0))
        surface.blit(text, (VIRTUAL_WIDTH // 2 - text.get_width() // 2, VIRTUAL_HEIGHT // 2 - text.get_height() // 2))

        font = self.fonts["medium_font"]
        text = font.render(f"Score: {self.score}", False, (255, 255, 255))
        surface.blit(text, (VIRTUAL_WIDTH // 2 - text.get_width() // 2, VIRTUAL_HEIGHT // 2 + 20))

        text = font.render("Press Return", False, (255, 255, 255))
        surface.blit(text, (VIRTUAL_WIDTH // 2 - text.get_width() // 2, VIRTUAL_HEIGHT // 2 + 60))