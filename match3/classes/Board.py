import random

from match3.classes.Tile import Tile
from match3.src.settings import BOARD_SIZE, TILE_SIZE
from match3.src.tween import create_pos_tween,ease_out_quad, TWEEN_DEFAULT_RATE, ShrinkSpinTween

class Board:

    # INIT, UPDATE, RENDER

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


    def update(self, dt):
        pass


    def render(self, surface, offset):

        for tile in self.tiles:
            tile.render(surface, offset)


    # HELPER METHODS


    def add_tile(self, row, col):
        """
        For a given row and column, creates a new Tile with a random colour
        and variety, whilst avoiding the creation of any immediate 3-in-a-row.
        """
        
        # colour and variety
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


    def initialise_tiles(self):
        """
        Creates a new board of Tiles which does not contain any matches.
        """
        self.tiles = []

        for row in range(self.rows):
            for col in range(self.cols):
                self.add_tile(row, col)


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
        empty_tiles = [tile for tile in self.tiles if tile.is_empty]

        return len(empty_tiles) > 0
    

    # TWEENING

    def create_drop_tween(self, tile, destination, duration=TWEEN_DEFAULT_RATE):
        tween = create_pos_tween(tile, tile.rect.topleft, destination, duration, None, ease_out_quad)
        self.tween_manager.add(tween)
        return tween
    

    # PLAYSTATE METHODS

    def swap_tiles(self, tile1: Tile, tile2: Tile):
        row1, col1 = tile1.row, tile1.col
        tile1.row, tile1.col = tile2.row, tile2.col
        tile2.row, tile2.col = row1, col1

        # start tweening to new positions
        tween1 = tile1.start_tween(tile2.rect.topleft)
        tween2 = tile2.start_tween(tile1.rect.topleft)

        self.tween_manager.add(tween1)
        self.tween_manager.add(tween2)

        self.sort_tiles()


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
        Removes matched tiles from the board with an animation tween and replaces the tiles
        with empty ones.
        """
        # iterate over a snapshot of keys so we can schedule tweens safely
        for (row, col) in list(self.matches.keys()):
            tile = self.get_tile(row, col)

            # on completion replace the tile with an empty tile
            def _on_complete(r=row, c=col):
                self.set_tile(r, c, Tile(c, r, self.asset_manager, -1, -1, True))

            shrink_spin_tween = ShrinkSpinTween(tile, TWEEN_DEFAULT_RATE, _on_complete, ease_out_quad)
            self.tween_manager.add(shrink_spin_tween)

        # clear matches immediately; actual removal happens when tweens complete
        self.matches = {}
    

    def drop_tile(self, tile, delta_rows):

        # define the tween
        new_pos = (tile.rect.x, tile.rect.y + delta_rows * TILE_SIZE)
        self.create_drop_tween(tile, new_pos, TWEEN_DEFAULT_RATE * delta_rows)

        # logical move
        tile.row += delta_rows


    def drop_column_tiles(self, non_empty_tiles, empty_rows):

        # place the non-empty tiles starting at row = empties
        for i, tile in enumerate(non_empty_tiles):
            target_row = empty_rows + i
            # compute how far it needs to drop
            delta = target_row - tile.row
            # set tile into new logical slot now so get_tile reflects upcoming state
            self.set_tile(target_row, tile.col, tile)
            if delta > 0:
                # schedule visual drop
                self.drop_tile(tile, delta)
            else:
                # ensure tile.row is correct if it wasn't moved
                tile.row = target_row


    def create_new_tiles(self, column: int, empty_rows: int):
        # create new tiles to fill the top empty_rows and drop them in
        for row in range(empty_rows):
            new_row = row
            new_tile = Tile(column,
                            new_row,
                            self.asset_manager,
                            random.randint(0, self.difficulty),
                            random.randint(0, self.difficulty))
            # position above the board so it can drop in
            new_tile.rect.topleft = (column * TILE_SIZE, - (empty_rows - row) * TILE_SIZE)

            # place the tile logically into its target slot, then animate it dropping in
            self.set_tile(new_row, column, new_tile)

            # animate the visual drop without altering the logical row
            self.create_drop_tween(
                new_tile,
                (column * TILE_SIZE, new_row * TILE_SIZE), 
                TWEEN_DEFAULT_RATE * empty_rows
                )


    def drop_tiles(self):
        """
        Finds empty tiles in each column, drops the tiles above into empty spaces, and creates new tiles to refill.
        """

        for col in range(self.cols):

            # collect current column top->bottom
            column_tiles = [self.get_tile(row, col) for row in range(self.rows)]

            # non-empty tiles in top->bottom order
            non_empty = [tile for tile in column_tiles if not tile.is_empty]

            empties = self.rows - len(non_empty)

            # if there are no empties in this column, continue
            if empties == 0:
                continue

            self.drop_column_tiles(non_empty, empties)

            self.create_new_tiles(col, empties)

        # check there are no empty tiles remaining
        assert(not self.has_empty_tiles())
