import random

from match3.classes.Tile import Tile
from match3.src.settings import BOARD_SIZE, TILE_SIZE

class Board:
    def __init__(self, x, y, asset_manager):
        self.asset_manager = asset_manager
        self.x = x
        self.y = y

        self.matches = {}
        self.initialise_tiles()


    def initialise_tiles(self):
        self.tiles = []

        for row in range(BOARD_SIZE):
            tile_row = []
            
            for col in range(BOARD_SIZE):
                tile_row.append(Tile(col, row, self.asset_manager, random.randint(0, 5), random.randint(0, 5)))
            
            self.tiles.append(tile_row)


    def update(self, dt):
        pass


    def check_matches(self):
        """
        Check the board for matches of 3 or more tiles of the same colour in a row or column.
        """

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                tile = self.tiles[row][col]
                colour = tile.colour

                # Check horizontal match
                if col <= BOARD_SIZE - 3:
                    if self.tiles[row][col + 1].colour == colour and self.tiles[row][col + 2].colour == colour:
                        self.matches[(row, col)] = True
                        self.matches[(row, col + 1)] = True
                        self.matches[(row, col + 2)] = True

                # Check vertical match
                if row <= BOARD_SIZE - 3:
                    if self.tiles[row + 1][col].colour == colour and self.tiles[row + 2][col].colour == colour:
                        self.matches[(row, col)] = True
                        self.matches[(row + 1, col)] = True
                        self.matches[(row + 2, col)] = True
                    
        return self.matches
    

    def remove_matches(self):
        for (row, col) in self.matches.keys():
            self.tiles[row][col] = None
            
            # drop tiles above
            for r in range(row - 1, -1, -1):
                if self.tiles[r][col] is not None:
                    # tween tile down
                    self.tiles[r][col].row += 1
                    self.tiles[r][col].start_tween((col * TILE_SIZE, (r + 1) * TILE_SIZE))
                    self.tiles[r + 1][col] = self.tiles[r][col]
                    self.tiles[r][col] = None

        self.matches = {}


    def replace_empty_tiles(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.tiles[row][col] is None:
                    self.tiles[row][col] = Tile(col, row, self.asset_manager, random.randint(0, 5), random.randint(0, 5))


    def render(self, surface, offset):

        for row in self.tiles:
            for tile in row:
                if tile is not None:
                    tile.render(surface, offset)
