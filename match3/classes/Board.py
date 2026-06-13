import random

from match3.classes.Tile import Tile
from match3.src.settings import BOARD_SIZE, TILE_SIZE
from match3.src.tween import create_pos_tween,ease_out_quad

class Board:
    def __init__(self, x, y, asset_manager, difficulty, tween_manager=None):
        self.x = x
        self.y = y

        self.asset_manager = asset_manager
        self.difficulty = difficulty
        self.tween_manager = tween_manager

        self.rows = BOARD_SIZE
        self.cols = BOARD_SIZE

        self.matches = {}
        self.initialise_tiles()


    def initialise_tiles(self):
        self.tiles = []

        for row in range(self.rows):
            for col in range(self.cols):
                # pick a colour and variety but avoid creating any immediate 3-in-a-row
                colour = random.randint(0, self.difficulty)
                variety = random.randint(0, self.difficulty)

                # while placing this tile would create a horizontal or vertical match,
                # pick a different colour/variety and try again
                while True:
                    creates_match = False

                    # check horizontal: look at two tiles to the left
                    if col >= 2:
                        left1 = self.get_tile(row, col - 1)
                        left2 = self.get_tile(row, col - 2)
                        if left1.colour == colour and left2.colour == colour:
                            creates_match = True

                    # check vertical: look at two tiles above
                    if row >= 2:
                        up1 = self.get_tile(row - 1, col)
                        up2 = self.get_tile(row - 2, col)
                        if up1.colour == colour and up2.colour == colour:
                            creates_match = True

                    if not creates_match:
                        break

                    # re-roll colour/variety and test again
                    colour = random.randint(0, self.difficulty)
                    variety = random.randint(0, self.difficulty)

                new_tile = Tile(col, row, self.asset_manager, colour, variety)
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


    def has_empty_tiles(self) -> bool:
        """
        Returns True if there are empty tiles in the board, False otherwise.
        """
        empty_tiles = False
        for col in range(self.cols):
            for row in range(self.rows):
                if self.get_tile(row, col).is_empty:
                    empty_tiles = True
                    break

        return empty_tiles
    

    def fill_empty_tiles(self):
        """
        Fills any empty tiles with a random Tile.
        """
        for col in range(self.cols):
            for row in range(self.rows):
                if self.get_tile(row, col).is_empty:
                    self.set_tile(
                        row,
                        col,
                        Tile(col,
                             row,
                             self.asset_manager,
                             random.randint(0, self.difficulty),
                             random.randint(0, self.difficulty)
                        )
                    )


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
        """
        Remove matched tiles from the board.
        """
        for (row, col) in self.matches.keys():
            self.set_tile(row, col, Tile(col, row, self.asset_manager, -1, -1, True))

        self.matches = {}


    def create_drop_tween(self, tile, destination):
        return create_pos_tween(tile, tile.rect.topleft, destination, 0.3, None)


    def move_tiles_down(self, col, row):
        # move tiles down in the specified column
        for r in range(row, 0, -1):
            self.set_tile(r, col, self.get_tile(r - 1, col))
            self.get_tile(r, col).row = r

            tweening_tile = self.get_tile(r, col)
            tween = self.create_drop_tween(tweening_tile, (col * TILE_SIZE, r * TILE_SIZE))
            self.tween_manager.add(tween)

        # add a new tile at the top of the column
        new_tile = Tile(col,
                        0,
                        self.asset_manager,
                        random.randint(0, self.difficulty),
                        random.randint(0, self.difficulty))
        self.set_tile(0, col, new_tile)

        # set position above the board
        new_tile.rect.topleft = (col * TILE_SIZE, - TILE_SIZE)
        tween_top = self.create_drop_tween(new_tile, (col * TILE_SIZE, 0))
        self.tween_manager.add(tween_top)


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
