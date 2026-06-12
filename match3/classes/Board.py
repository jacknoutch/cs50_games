import random

from match3.classes.Tile import Tile
from match3.src.settings import BOARD_SIZE
from match3.src.utils import debug

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


    def get_tile(self, row, col):
        # 0,0 is top-left
        return self.tiles[row * self.cols + col]


    def set_tile(self, row, col, tile):
        # 0,0 is top-left
        self.tiles[row * self.cols + col] = tile


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
            self.set_tile(row, col, Tile(col, row, self.asset_manager, -1, -1, True))

        self.matches = {}


    def move_tiles_down(self, col, row):
        # move tiles down in the specified column
        for r in range(row, 0, -1):
            self.set_tile(r, col, self.get_tile(r - 1, col))
            self.get_tile(r, col).row = r
            self.get_tile(r, col).start_tween((col * 32, r * 32))

        # add a new tile at the top of the column
        self.set_tile(0, col, Tile(col, 0, self.asset_manager, random.randint(0, 5), random.randint(0, 5)))
        self.get_tile(0, col).rect.topleft = (col * 32, -32) # set position above the board
        self.get_tile(0, col).start_tween((col * 32, 0))

        pass

    def replace_empty_tiles(self) -> bool:
        """
        For each column, drop tiles one move and spawn a new tile at the top.

        Returns True if any tiles were replaced, False otherwise.
        """

        empty_tiles = False

        for col in range(self.cols):
            for row in range(self.rows - 1, -1, -1):
                if self.get_tile(row, col).is_empty:
                    empty_tiles = True
                    self.move_tiles_down(col, row)
                    print("moved tile")
                    break

        if empty_tiles:
            print("Replaced empty tiles")
        else:
            print("No empty tiles to replace")

        return empty_tiles

    def render(self, surface, offset):

        for tile in self.tiles:
            tile.render(surface, offset)
