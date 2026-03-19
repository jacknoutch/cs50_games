import pygame as pg

from match3.classes.Board import Board
from match3.classes.states.BaseState import BaseState
from match3.src.settings import BOARD_OFFSET, BOARD_SIZE, TILE_SIZE

class PlayState(BaseState):

    def __init__(self):
        super().__init__()


    def enter(self):
        self.game = self.state_machine.game
        if self.game.debug:
            print("Entered state: " + self.__class__.__name__)
        
        self.board = Board(0, 0, self.game.asset_manager)
        
        self.cursor_active = True
        self.cursor_row = 0
        self.cursor_col = 0

        self.selected_tile = None
        self.pending_tween_tiles = None


    def update(self, dt):

        for tile in self.board.tiles:
            if tile is not None:
                tile.update(dt)

        if self.pending_tween_tiles is not None:
            tile1, tile2 = self.pending_tween_tiles
            if not tile1.tweening and not tile2.tweening:
                self.pending_tween_tiles = None
                if self.board.check_matches():
                    print("Match found!")
                    self.board.remove_matches() 
                    self.board.replace_empty_tiles()
            self.cursor_active = False
        else:
            self.cursor_active = True



        for event in self.game.events:

            if event.type == pg.QUIT:
                self.game.running = False

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    self.game.state_machine.change_state("start")

                if event.key == pg.K_DOWN:
                    self.move_cursor(1, 0)
                if event.key == pg.K_UP:
                    self.move_cursor(-1, 0)
                if event.key == pg.K_LEFT:
                    self.move_cursor(0, -1)
                if event.key == pg.K_RIGHT:
                    self.move_cursor(0, 1)

                if event.key == pg.K_RETURN:
                    if self.pending_tween_tiles is None:
                        self.handle_selection()


    def handle_selection(self):
        cursor_tile = self.board.tiles[self.cursor_row * self.board.cols + self.cursor_col]
        if self.selected_tile is None:
            self.select_tile()
        elif self.selected_tile == cursor_tile:
            self.selected_tile = None
        elif (abs(self.selected_tile.row - self.cursor_row) + abs(self.selected_tile.col - self.cursor_col)) == 1:
            self.swap_tiles(self.selected_tile, cursor_tile)
            self.selected_tile = None
        else:
            self.select_tile()

    
    def swap_tiles(self, tile1, tile2):
        row1, col1 = tile1.row, tile1.col
        tile1.row, tile1.col = tile2.row, tile2.col
        tile2.row, tile2.col = row1, col1

        # start tweening to new positions
        tile1.start_tween((tile1.col * TILE_SIZE, tile1.row * TILE_SIZE))
        tile2.start_tween((tile2.col * TILE_SIZE, tile2.row * TILE_SIZE))

        self.pending_tween_tiles = (tile1, tile2)


    def move_cursor(self, d_row, d_col):
        if self.cursor_active:
            self.cursor_row = (self.cursor_row + d_row) % self.board.rows
            self.cursor_col = (self.cursor_col + d_col) % self.board.cols


    def select_tile(self):
        if self.cursor_active:
            self.selected_tile = self.board.tiles[self.cursor_row * self.board.cols + self.cursor_col]
            print(f"Selected tile at row {self.cursor_row}, col {self.cursor_col} with colour {self.selected_tile.colour} and variety {self.selected_tile.variety}")


    def render(self, surface):
        self.board.render(surface, BOARD_OFFSET)

        self.render_cursor(surface)
        self.render_selected_tile(surface)


    def render_cursor(self, surface):
        pg.draw.rect(surface,
                     (255, 255, 255),
                     (BOARD_OFFSET[0] + self.cursor_col * TILE_SIZE, BOARD_OFFSET[1] + self.cursor_row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
        
    
    def render_selected_tile(self, surface):
        if self.selected_tile is not None:
            pg.draw.rect(surface,
                         (255, 255, 0),
                         (BOARD_OFFSET[0] + self.selected_tile.col * TILE_SIZE + 4, BOARD_OFFSET[1] + self.selected_tile.row * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8), 2)