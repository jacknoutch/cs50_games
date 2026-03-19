import random

from match3.classes.Tile import Tile
from match3.src.settings import BOARD_SIZE, TILE_SIZE

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
        # for (row, col) in self.matches.keys():
        #     self.tiles[row][col] = None
            
        #     # drop tiles above
        #     for r in range(row - 1, -1, -1):
        #         if self.tiles[r][col] is not None:
        #             # tween tile down
        #             self.tiles[r][col].row += 1
        #             self.tiles[r][col].start_tween((col * TILE_SIZE, (r + 1) * TILE_SIZE))
        #             self.tiles[r + 1][col] = self.tiles[r][col]
        #             self.tiles[r][col] = None

        # self.matches = {}
        pass


    def replace_empty_tiles(self):
        # for row in range(self.rows):
        #     for col in range(self.cols):
        #         if self.tiles[row][col] is None:
        #             self.tiles[row][col] = Tile(col, row, self.asset_manager, random.randint(0, 5), random.randint(0, 5))
        pass


    def render(self, surface, offset):

        for tile in self.tiles:
            tile.render(surface, offset)
