import random

from match3.classes.Tile import Tile
from match3.src.settings import BOARD_SIZE, TILE_SIZE
from match3.src.tween import create_pos_tween,ease_out_quad, TWEEN_DEFAULT_RATE

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
        self.tiles = []

        for row in range(self.rows):
            for col in range(self.cols):
                self.add_tile(row, col)


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
        Remove matched tiles from the board by animating them shrinking to their central point
        while spinning 360 degrees, then replacing them with an empty tile when the animation completes.
        """
        # iterate over a snapshot of keys so we can schedule tweens safely
        for (row, col) in list(self.matches.keys()):
            tile = self.get_tile(row, col)

            # on completion replace the tile with an empty tile
            def _on_complete(r=row, c=col):
                self.set_tile(r, c, Tile(c, r, self.asset_manager, -1, -1, True))

            # create a shrink+spin tween that scales the tile down to 0 while rotating it 360deg,
            # keeping its center fixed.
            class _ShrinkSpinTween:
                def __init__(self, tile, duration, on_complete, easing):
                    self.tile = tile
                    self.duration = duration
                    self.on_complete = on_complete
                    self.easing = easing

                    self.elapsed = 0.0
                    self.start_w = tile.rect.width
                    self.start_h = tile.rect.height
                    # ensure tile has scale/rotation properties used by Tile.render
                    if not hasattr(tile, 'scale'):
                        tile.scale = 1.0
                    if not hasattr(tile, 'rotation'):
                        tile.rotation = 0.0
                    self.center = tile.rect.center
                    self.finished = False

                def update(self, dt):
                    if self.finished:
                        return

                    self.elapsed += dt
                    t = min(1.0, self.elapsed / self.duration)
                    eased = self.easing(t)

                    # scale goes from 1.0 -> 0.0, rotation from 0 -> 360
                    new_scale = max(0.0, 1.0 - eased)
                    new_rotation = eased * 180.0

                    # apply to tile (Tile.render should respect these)
                    self.tile.scale = new_scale
                    self.tile.rotation = new_rotation

                    # also keep rect sized to scaled dimensions so other logic / collision works
                    new_w = max(0, int(self.start_w * new_scale))
                    new_h = max(0, int(self.start_h * new_scale))

                    cx, cy = self.center
                    # when size becomes 0 we still want rect centered at same point
                    if new_w == 0: new_w = 1
                    if new_h == 0: new_h = 1

                    self.tile.rect.width = new_w
                    self.tile.rect.height = new_h
                    self.tile.rect.topleft = (cx - new_w // 2, cy - new_h // 2)

                    if t >= 1.0:
                        self.finished = True
                        # reset visual properties to defaults before replacing tile
                        self.tile.scale = 1.0
                        self.tile.rotation = 0.0
                        if self.on_complete:
                            self.on_complete()

                @property
                def done(self):
                    return self.finished

            duration = TWEEN_DEFAULT_RATE
            shrink_spin_tween = _ShrinkSpinTween(tile, duration, _on_complete, ease_out_quad)

            if self.tween_manager:
                self.tween_manager.add(shrink_spin_tween)
            else:
                # if no tween manager, immediately replace tile
                _on_complete()

        # clear matches immediately; actual removal happens when tweens complete
        self.matches = {}


    def create_drop_tween(self, tile, destination):
        return create_pos_tween(tile, tile.rect.topleft, destination, TWEEN_DEFAULT_RATE, None, ease_out_quad)


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


    def calculate_delta_row(self, tile: Tile):
        # how many empty spaces are there under this tile?
        print(f"tile row: {tile.row}")
        column_below = [t for t in self.tiles if t.col == tile.col]
        print(f"column below: {column_below}")
        empty_tiles_below = [t for t in column_below if t.is_empty]
        print(f"empty tiles below: {empty_tiles_below}")

        return len(empty_tiles_below)
    

    def drop_tile(self, tile, delta_rows):

        # define the tween
        old_pos = tile.rect.topleft
        new_pos = (tile.rect.x, tile.rect.y + delta_rows * TILE_SIZE)

        tween = create_pos_tween(
            tile,
            old_pos,
            new_pos,
            duration=TWEEN_DEFAULT_RATE * delta_rows,
            on_complete=None,
            easing=ease_out_quad
        )

        self.tween_manager.add(tween)

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
            # set into board
            self.set_tile(new_row, column, new_tile)

            # compute drop distance in rows for the new tile: it always travels 'empty_rows'
            drop_rows = empty_rows
            duration = TWEEN_DEFAULT_RATE * drop_rows

            # create tween that matches the same per-row speed as other drops
            tween = create_pos_tween(new_tile,
                                        new_tile.rect.topleft,
                                        (column * TILE_SIZE, new_row * TILE_SIZE),
                                        duration=duration,
                                        on_complete=None,
                                        easing=ease_out_quad)
            self.tween_manager.add(tween)



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
        empty_tiles = [tile for tile in self.tiles if tile.is_empty]
        assert(len(empty_tiles) == 0)


    def render(self, surface, offset):

        for tile in self.tiles:
            tile.render(surface, offset)
