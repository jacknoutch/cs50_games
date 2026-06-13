import pygame as pg

from match3.classes.Board import Board
from match3.classes.Tile import Tile
from match3.classes.states.BaseState import BaseState
from match3.src.settings import BOARD_OFFSET, DEFAULT_COUNTDOWN_LENGTH, TILE_SIZE, MARGIN, VIRTUAL_HEIGHT

class PlayState(BaseState):

    def __init__(self):
        super().__init__()

        # left side background (similar to StartState menu_background)
        # covers the left side of the screen where score and timer are displayed
        left_panel_width = BOARD_OFFSET[0] - MARGIN * 2
        left_panel_height = VIRTUAL_HEIGHT - MARGIN * 2
        self.left_background_surf = pg.Surface((left_panel_width, left_panel_height - MARGIN * 4), pg.SRCALPHA)
        self.left_background_surf.fill((0, 0, 0, 127))


    def enter(self):
        self.game = self.state_machine.game
        if self.game.debug:
            print("Entered state: " + self.__class__.__name__)
        
        self.game.score = 0

        self.board = Board(0, 0,
                           self.game.asset_manager,
                           self.game.difficulty,
                           self.game.tween_manager)

        self.cursor_active = True
        self.cursor_row = 0
        self.cursor_col = 0

        self.selected_tile = None

        self.pending_tweening = False
        self.empty_tiles = False

        # countdown in seconds
        self.countdown = DEFAULT_COUNTDOWN_LENGTH


    def update(self, dt):

        for tile in self.board.tiles:
            if tile is not None:
                tile.update(dt)

        # update countdown timer and exit to StartState when it reaches zero
        self.countdown -= dt
        if self.countdown <= 0:
            # time's up -> go back to the start screen
            self.game.state_machine.change_state("start")
            return

        # tweening
        if self.pending_tweening:
            self.cursor_active = False

            if not self.game.tween_manager.any():
                self.pending_tweening = False

        # empty tiles
        elif self.empty_tiles:
            self.empty_tiles = self.board.replace_empty_tiles()
            self.pending_tweening = True

        # matches present
        elif self.board.check_matches():
            print("Match found!")
            self.score_match()
            self.countdown += 1
            self.board.remove_matches()
            self.empty_tiles = True

        # user may interact
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
                    if not self.pending_tweening:
                        self.handle_selection()

    
    def handle_selection(self):
        cursor_tile = self.board.tiles[self.cursor_row * self.board.cols + self.cursor_col]

        # select
        if self.selected_tile is None:
            self.select_tile()
        
        # unselect
        elif self.selected_tile == cursor_tile:
            self.selected_tile = None

        # swap tile (select tile next to existing selection)
        elif (abs(self.selected_tile.row - self.cursor_row) + abs(self.selected_tile.col - self.cursor_col)) == 1:
            self.swap_tiles(self.selected_tile, cursor_tile)
            self.selected_tile = None
        
        # other
        else:
            self.select_tile()


    def score_match(self):
        """
        Calculate score from current board.matches.
        Groups of contiguous matched tiles are scored:
        3 -> 30, 4 -> 50, 5+ -> 100.
        """
        matches = self.board.matches
        if not matches:
            return

        visited = set()

        for pos in list(matches.keys()):
            if pos in visited:
                continue

            # flood fill to find contiguous group size
            stack = [pos]
            visited.add(pos)
            group_size = 0

            while stack:
                r, c = stack.pop()
                group_size += 1

                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if (nr, nc) in matches and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        stack.append((nr, nc))

            # award points based on group size
            if group_size == 3:
                self.game.score += 30
            elif group_size == 4:
                self.game.score += 50
            elif group_size >= 5:
                self.game.score += 100


    def swap_tiles(self, tile1: Tile, tile2: Tile):
        row1, col1 = tile1.row, tile1.col
        tile1.row, tile1.col = tile2.row, tile2.col
        tile2.row, tile2.col = row1, col1

        # start tweening to new positions
        tween1 = tile1.start_tween(tile2.rect.topleft)
        tween2 = tile2.start_tween(tile1.rect.topleft)

        self.game.tween_manager.add(tween1)
        self.game.tween_manager.add(tween2)

        self.pending_tweening = True
        self.board.sort_tiles()


    def move_cursor(self, d_row: int, d_col: int):
        if self.cursor_active:
            self.cursor_row = (self.cursor_row + d_row) % self.board.rows
            self.cursor_col = (self.cursor_col + d_col) % self.board.cols


    def select_tile(self):
        if self.cursor_active:
            self.selected_tile = self.board.tiles[self.cursor_row * self.board.cols + self.cursor_col]
            print(f"Selected tile at row {self.cursor_row}, col {self.cursor_col} with colour {self.selected_tile.colour} and variety {self.selected_tile.variety}")


    def render(self, surface):
        # draw semi-transparent background on left side
        surface.blit(self.left_background_surf, (MARGIN, MARGIN))

        # draw board
        self.board.render(surface, BOARD_OFFSET)

        # draw score on left side
        font = self.game.asset_manager.get_font("font", 24)
        score_surf = font.render(f"Score: {self.game.score}", False, (255, 255, 255))
        surface.blit(score_surf, (MARGIN, MARGIN))

        # render countdown below the score
        timer_surf = font.render(f"Time: {int(self.countdown)}", False, (255, 255, 255))
        surface.blit(timer_surf, (MARGIN, MARGIN + 28))

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
                         (BOARD_OFFSET[0] + self.selected_tile.col * TILE_SIZE + 4,
                          BOARD_OFFSET[1] + self.selected_tile.row * TILE_SIZE + 4,
                          TILE_SIZE - 8,
                          TILE_SIZE - 8),
                          2)