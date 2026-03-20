import random

from match3.classes.Tile import Tile
from match3.src.settings import BOARD_SIZE

class Board:
    def __init__(self, x, y, asset_manager):
        self.asset_manager = asset_manager
        self.x = x
        self.y = y

        self.rows = BOARD_SIZE
        self.cols = BOARD_SIZE

        self.matches = {}
        self.initialise_tiles()


    def initialise_tiles(self):
        self.tiles = []

        for row in range(self.rows):
            for col in range(self.cols):
                new_tile = Tile(col, row, self.asset_manager, random.randint(0, 5), random.randint(0, 5))
                self.tiles.append(new_tile)


    def update(self, dt):
        pass


    def sort_tiles(self):
        self.tiles.sort(key=lambda tile: (tile.row, tile.col))


    def check_matches(self):
        """
        Check the board for matches of 3 or more tiles of the same colour in a row or column.
        """

        for i, tile in enumerate(self.tiles):
            colour = tile.colour

            # Check horizontal match
            if tile.col <= self.cols - 3:
                if self.tiles[i + 1].colour == colour and self.tiles[i + 2].colour == colour:
                    self.matches[(tile.row, tile.col)] = True
                    self.matches[(tile.row, tile.col + 1)] = True
                    self.matches[(tile.row, tile.col + 2)] = True

            # Check vertical match
            if tile.row <= self.rows - 3:
                if self.tiles[i + self.cols].colour == colour and self.tiles[i + 2 * self.cols].colour == colour:
                    self.matches[(tile.row, tile.col)] = True
                    self.matches[(tile.row + 1, tile.col)] = True
                    self.matches[(tile.row + 2, tile.col)] = True

        return self.matches
    

    def remove_matches(self):
        for (row, col) in self.matches.keys():
            self.tiles[row * self.cols + col] = Tile(col, row, self.asset_manager, -1, -1, True)

        self.matches = {}


    def replace_empty_tiles(self):
        # for row in range(self.rows):
        #     for col in range(self.cols):
        #         if self.tiles[row][col] is None:
        #             self.tiles[row][col] = Tile(col, row, self.asset_manager, random.randint(0, 5), random.randint(0, 5))
        pass


    def render(self, surface, offset):

        for tile in self.tiles:
            tile.render(surface, offset)
