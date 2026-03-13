import pygame as pg

from breakout.classes.Ball import Ball
from breakout.classes.LevelMaker import LevelMaker
from breakout.classes.Paddle import Paddle
from breakout.classes.states.BaseState import BaseState
from breakout.src.settings import VIRTUAL_HEIGHT

class PlayState(BaseState):
    def __init__(self):
        super().__init__()

        self.colour = "blue"
        self.size = "medium"
        self.player = None
        self.ball = None
        self.bricks = None
        self.paused = False


    def enter(self, player, ball, bricks, score):
        print("Entering Play State")
        self.player = player
        self.ball = ball
        self.bricks = bricks
        self.health = self.state_machine.game.health
        self.score = score
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

        if self.ball.rect.bottom >= VIRTUAL_HEIGHT:
            self.state_machine.game.health -= 1
            if self.state_machine.game.health <= 0:
                self.state_machine.change_state("start")
            else:
                self.state_machine.change_state("serve")

        self.player.update(dt)
        self.ball.update(dt)

        collision = self.ball.collide(self.player, dt)
        if collision:
            self.ball.bounce(collision, self.player)


        for brick in self.bricks[:]:
            collision = self.ball.collide(brick)
            if collision:
                self.ball.bounce(collision, brick)
                self.bricks.remove(brick)



    def render(self, surface):
        self.player.render(surface)
        self.ball.render(surface)

        for brick in self.bricks:
            brick.render(surface)

        if self.state_machine.game.debug:
            pg.draw.rect(surface, (255, 0, 0), self.player.rect, 1)
            pg.draw.rect(surface, (255, 0, 0), self.ball.rect, 1)
            self.state_machine.game.debug_info(f"Ball Speed: {self.ball.speed}", surface, 1, 20)

        self.state_machine.game.render_hearts()