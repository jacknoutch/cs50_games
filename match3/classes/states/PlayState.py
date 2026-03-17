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


    def update(self, dt):

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
                    self.handle_selection()


    def handle_selection(self):
        if self.selected_tile is None:
            self.select_tile()
        elif self.selected_tile == self.board.tiles[self.cursor_row][self.cursor_col]:
            self.selected_tile = None
        elif (abs(self.selected_tile.row - self.cursor_row) + abs(self.selected_tile.col - self.cursor_col)) == 1:
            print(f"Swapping tile at row {self.selected_tile.row}, col {self.selected_tile.col} with tile at row {self.cursor_row}, col {self.cursor_col}")
            self.swap_tiles(self.selected_tile, self.board.tiles[self.cursor_row][self.cursor_col])
            self.selected_tile = None
        else:
            self.select_tile()

    
    def swap_tiles(self, tile1, tile2):
        # swap positions in board
        self.board.tiles[tile1.row][tile1.col], self.board.tiles[tile2.row][tile2.col] = self.board.tiles[tile2.row][tile2.col], self.board.tiles[tile1.row][tile1.col]

        # swap row and col attributes
        tile1.row, tile2.row = tile2.row, tile1.row
        tile1.col, tile2.col = tile2.col, tile1.col

        # update rect positions
        tile1.rect.topleft = (tile1.col * TILE_SIZE, tile1.row * TILE_SIZE)
        tile2.rect.topleft = (tile2.col * TILE_SIZE, tile2.row * TILE_SIZE)

        if self.board.check_matches():
            print("Match found!")
            self.board.remove_matches() 
            self.board.replace_empty_tiles()

    def move_cursor(self, d_row, d_col):
        if self.cursor_active:
            self.cursor_row = (self.cursor_row + d_row) % BOARD_SIZE
            self.cursor_col = (self.cursor_col + d_col) % BOARD_SIZE


    def select_tile(self):
        if self.cursor_active:
            self.selected_tile = self.board.tiles[self.cursor_row][self.cursor_col]
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