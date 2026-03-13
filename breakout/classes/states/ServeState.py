import pygame as pg

from breakout.classes.Ball import Ball
from breakout.classes.LevelMaker import LevelMaker
from breakout.classes.Paddle import Paddle
from breakout.classes.states.BaseState import BaseState

class ServeState(BaseState):
    def __init__(self):
        super().__init__()

        self.colour = "blue"
        self.size = "small"

    def enter(self, bricks=None):
        print("Entering Serve State")

        brick_assets = {
            "sprites": self.state_machine.game.brick_sprites,
            "sfx": self.state_machine.game.assets.sounds["brick-hit-1"]
        }

        self.bricks = bricks if bricks is not None else LevelMaker.create_map(brick_assets)

        player_sprite = self.state_machine.game.paddle_sprites[self.colour][self.size]
        self.player = Paddle(self.colour, self.size, player_sprite)
        ball_sounds = {
            "wall_hit": self.state_machine.game.assets.sounds["wall_hit"],
            "paddle_hit": self.state_machine.game.assets.sounds["paddle_hit"],
            "brick-hit-2": self.state_machine.game.assets.sounds["brick-hit-2"]
        }
        self.ball = Ball(self.state_machine.game.ball_sprites["red"], ball_sounds)
        self.ball.reset()

    def exit(self):
        print("Exiting Serve State")

    def update(self, dt):
        events = self.state_machine.game.events

        for event in events:

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.state_machine.change_state("start")

                if event.key == pg.K_RETURN:
                    self.state_machine.change_state("play",
                                                    self.player,
                                                    self.ball,
                                                    self.bricks)

    def render(self, surface):
        self.player.render(surface)
        self.ball.render(surface)

        for brick in self.bricks:
            brick.render(surface)

        self.state_machine.game.render_hearts()