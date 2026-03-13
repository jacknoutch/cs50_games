import pygame as pg

from breakout.classes.states.BaseState import BaseState
from breakout.src.settings import VIRTUAL_HEIGHT, VIRTUAL_WIDTH

class StartState(BaseState):
    def __init__(self):
        super().__init__()

        self.selection = 0
        self.choices = ["Start", "High Scores", "Quit"]

    def enter(self):
        print("Entering Start State")

    def exit(self):
        print("Exiting Start State")

    def update(self, dt):
        events = self.state_machine.game.events

        for event in events:

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    self.selection = (self.selection + 1) % len(self.choices)
                    self.state_machine.game.assets.get_sound("paddle_hit").play()

                if event.key == pg.K_UP:
                    self.selection = (self.selection - 1) % len(self.choices)
                    self.state_machine.game.assets.get_sound("paddle_hit").play()

                if event.key == pg.K_ESCAPE:
                    self.state_machine.game.running = False

                if event.key == pg.K_RETURN:
                    self.select_choice()


    def render(self, surface):

        font = self.state_machine.game.assets.get_font("large_font")

        title = font.render("BREAKOUT", True, (255, 255, 255))
        title_rect = title.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 4))
        surface.blit(title, title_rect)

        for i, choice in enumerate(self.choices):
            color = (255, 255, 255) if i == self.selection else (100, 100, 100)
            text = font.render(choice, True, color)
            text_rect = text.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2 + i * 30))
            surface.blit(text, text_rect)


    def select_choice(self):
        choice = self.choices[self.selection]
        if choice == "Start":
            self.state_machine.change_state("serve")
        elif choice == "High Scores":
            self.state_machine.change_state("high_scores")
        elif choice == "Quit":
            self.state_machine.game.running = False