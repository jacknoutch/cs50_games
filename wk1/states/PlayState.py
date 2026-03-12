import pygame as pg
import random

from wk1.assets import assets
from wk1.states.BaseState import BaseState
from wk1.Bird import Bird
from wk1.PipePair import PipePair
from wk1.settings import PIPE_GAP, PIPE_SCROLL_SPEED, PIPE_SPAWN_INTERVAL, PIPE_HEIGHT, PIPE_WIDTH, VIRTUAL_HEIGHT

class PlayState(BaseState):
    def __init__(self):
        super().__init__()

        self.bird = Bird()
        self.pipe_pairs = []
        self.spawn_timer = 0
        self.score = 0

        # initialise the last recorded y value of the pipe pair, ensuring it spawns within the screen bounds
        self.previous_pipe_y = -PIPE_HEIGHT + random.randint(0, 80) + 20

    def update(self, dt: float, keys_pressed: pg.key.ScancodeWrapper):

        # Spawn new pipe pairs

        self.spawn_timer += dt

        if self.spawn_timer > PIPE_SPAWN_INTERVAL:

            # determine the y position of the new pipe pair
            # the pair (and gap) will be 20 pixels higher or lower than previously
            # but no higher than 10 pixels below the top of the screen and no lower than a gap height from the bottom
            y = max(-PIPE_HEIGHT + 10, 
                    min(self.previous_pipe_y + random.randint(-20, 20),
                        VIRTUAL_HEIGHT - PIPE_HEIGHT - PIPE_GAP))
            self.previous_pipe_y = y

            # add spawn a new pipe pair at y
            self.pipe_pairs.append(PipePair(y=y))

            # reset the spawn timer
            self.spawn_timer = 0


        # Bird

        self.bird.update(dt, keys_pressed=keys_pressed)

        if self.bird.rect.bottom > VIRTUAL_HEIGHT or self.bird.rect.top < 0:
            self.state_machine.change_state('score', score=self.score)

        # Pipe pairs

        for pipe_pair in self.pipe_pairs[:]:

            pipe_pair.update(dt)

            if pipe_pair.x + PIPE_WIDTH < self.bird.rect.x and not pipe_pair.scored:
                self.score += 1
                pipe_pair.scored = True

            for pipe in pipe_pair.pipes.values():
                if self.bird.collides(pipe):
                    self.state_machine.change_state('score', score=self.score)

            if pipe_pair.remove:
                self.pipe_pairs.remove(pipe_pair)


    def render(self, surface):

        for pipe_pair in self.pipe_pairs:
            pipe_pair.render(surface)
            
        self.bird.render(surface)

        text = assets.flappy_font.render(f"Score: {self.score}", False, (255, 255, 255))
        surface.blit(text, (10, 10))