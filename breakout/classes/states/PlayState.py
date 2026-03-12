import pygame as pg

from breakout.classes.Paddle import Paddle
from breakout.classes.states.BaseState import BaseState

class PlayState(BaseState):
    def __init__(self):
        super().__init__()

        self.colour = "blue"
        self.size = "medium"
        self.player = None
        self.paused = False

    def enter(self):
        print("Entering Play State")
        self.sprite = self.state_machine.game.paddle_sprites[self.colour][self.size]
        self.player = Paddle(self.colour, self.size, self.sprite)

    def exit(self):
        print("Exiting Play State")

    def update(self, dt):
        keys_pressed = self.state_machine.game.keys_pressed
        events = self.state_machine.game.events

        for event in events:

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.state_machine.change_state("start")

                if event.key == pg.K_SPACE:
                    self.paused = not self.paused
                    self.state_machine.game.assets.sounds["pause"].play()
                    
        if self.paused:
            return

        if keys_pressed[pg.K_LEFT]:
            self.player.move(-1)
        elif keys_pressed[pg.K_RIGHT]:
            self.player.move(1)
        else:
            self.player.stop()

        self.player.update(dt)

    def render(self, surface):
        self.player.render(surface)