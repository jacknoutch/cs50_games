import pygame as pg

from breakout.classes.Ball import Ball
from breakout.classes.LevelMaker import LevelMaker
from breakout.classes.Paddle import Paddle
from breakout.classes.states.BaseState import BaseState

class PlayState(BaseState):
    def __init__(self):
        super().__init__()

        self.colour = "blue"
        self.size = "medium"
        self.player = None
        self.ball = None
        self.paused = False


    def enter(self):
        print("Entering Play State")
        brick_assets = {
            "sprites": self.state_machine.game.brick_sprites,
            "sfx": self.state_machine.game.assets.sounds["brick-hit-1"]
        }
        self.bricks = LevelMaker.create_map(brick_assets)
        
        player_sprite = self.state_machine.game.paddle_sprites[self.colour][self.size]
        self.player = Paddle(self.colour, self.size, player_sprite)
        self.ball = Ball(self.state_machine.game.ball_sprites["red"], self.state_machine.game.assets.sounds["wall_hit"])
        self.ball.reset()
        self.ball.start()

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

        if self.ball.collide(self.player):
            self.ball.bounce()
            self.state_machine.game.assets.sounds["paddle_hit"].play()

        for brick in self.bricks:
            collision = self.ball.collide(brick)
            if collision:
                self.ball.bounce()
                self.state_machine.game.assets.sounds["brick-hit-2"].play()
                self.bricks.remove(brick)

        self.player.update(dt)
        self.ball.update(dt)


    def render(self, surface):
        self.player.render(surface)
        self.ball.render(surface)

        for brick in self.bricks:
            brick.render(surface)

        if self.state_machine.game.debug:
            pg.draw.rect(surface, (255, 0, 0), self.player.rect, 1)
            pg.draw.rect(surface, (255, 0, 0), self.ball.rect, 1)