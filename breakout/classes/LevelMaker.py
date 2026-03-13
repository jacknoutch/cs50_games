import pygame as pg

from breakout.classes.Brick import Brick

class LevelMaker:

    @staticmethod
    def create_map(brick_assets):
        bricks = []
        for row in range(5):
            for col in range(10):
                brick = Brick(brick_assets["sprites"])
                brick.rect.topleft = (col * 62, row * 22)
                bricks.append(brick)
        return bricks