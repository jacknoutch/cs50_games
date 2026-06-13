import pygame as pg
import random

from match3.assets.AssetManager import TILE_COLUMN_COUNT, TILE_ROW_COUNT, TILE_SIZE
from match3.classes.states.BaseState import BaseState
from match3.src.settings import BOARD_OFFSET, MARGIN, VIRTUAL_HEIGHT, VIRTUAL_WIDTH
from match3.src.tween import Tween, ease_out_quad

class StartState(BaseState):

    def __init__(self):
        super().__init__()


        # flashing title
        self.current_colour = 0
        self.colours = [
            (217, 87, 99),
            (95, 205, 228),
            (251, 242, 54),
            (118, 66, 138),
            (153, 229, 80),
            (223, 113, 38)
        ]


        # define a custom event to flash each letter every 75 ms
        self.title_flash = pg.event.custom_type()
        pg.time.set_timer(self.title_flash, 75)
        
        
        # menu
        self.menu_options = ["Start Game", "Options", "Quit"]
        self.selected_option = 0

        # menu_background
        self.menu_background_surf = pg.Surface((VIRTUAL_WIDTH - MARGIN * 2, VIRTUAL_HEIGHT - MARGIN * 6), pg.SRCALPHA)
        self.menu_background_surf.fill((0, 0, 0, 127))

        # tween to other states
        self.fade_duration = 0.5 # seconds
        self.overlay_alpha = 0.0


    def enter(self):
        self.game = self.state_machine.game
        if self.game.debug:
            print("Entered state: " + self.__class__.__name__)

        # tiles
        self.tiles = []
        for i in range(64):
            tile_sprites = self.game.asset_manager.get_image("tiles")
            tile = tile_sprites[random.randint(0, TILE_ROW_COUNT - 1)][random.randint(0, TILE_COLUMN_COUNT - 1)]
            self.tiles.append(tile)


    def update(self, dt):

        for event in self.game.events:

            if event.type == pg.QUIT:
                self.game.running = False

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    self.game.running = False
                if event.key == pg.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                if event.key == pg.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                if event.key == pg.K_RETURN:
                    self.select_option()

            if event.type == self.title_flash:
                self.current_colour = (self.current_colour + 1) % len(self.colours)


    def render(self, surface):

        font = self.game.asset_manager.get_font("font", 36)
        surface.blit(self.menu_background_surf, (MARGIN, MARGIN))
        self.render_title(surface, font)
        self.render_menu(surface, font)
        self.render_tiles(surface)

        if self.game.score is not None and type(self.game.score) == int:
            score_text = f"Score: {self.game.score}"
            score_surf = font.render(score_text, False, (255, 255, 255))
            surface.blit(score_surf, (VIRTUAL_WIDTH - MARGIN - score_surf.get_width(), MARGIN))


    def render_title(self, surface, font):

        x, y = 100, 50

        letter_table = {
            "M": (0, 0),
            "A": (30, 0),
            "T": (54, 0),
            "C": (74, 0),
            "H": (96, 0),
            "3": (122, 0)
        }

        for i, (letter, pos) in enumerate(letter_table.items()):
            letter_surface = font.render(letter, False, self.colours[(i + self.current_colour) % len(self.colours)])
            surface.blit(letter_surface, (x + pos[0], y + pos[1]))


    def render_menu(self, surface, font):

        for i, option in enumerate(self.menu_options):
            if i == self.selected_option:
                text = font.render(option, False, (255, 255, 255))
            else:
                text = font.render(option, False, (128, 128, 128))
            surface.blit(text, (100, 100 + i * 40))


    def select_option(self):
        
        option = self.menu_options[self.selected_option]
        if option == "Start Game":
            print("Start Game selected")

            def update_fn(t):
                self.overlay_alpha = int(255 * t)

            def on_complete():
                self.overlay_alpha = 255
                self.state_machine.change_state("play")
                self.overlay_alpha = 0


            tween = Tween(self.fade_duration, update_fn, on_complete=on_complete, easing=ease_out_quad)
            self.game.tween_manager.add(tween)

        elif option == "Options":
            print("Options selected")
            # self.state_machine.change_state("options")  # TODO: implement OptionsState
        elif option == "Quit":
            print("Quit selected")
            self.game.running = False


    def render_tiles(self, surface):
        x, y = BOARD_OFFSET
        for i, tile in enumerate(self.tiles):
            surface.blit(tile, (x + i % 8 * TILE_SIZE, y + i // 8 * TILE_SIZE))

        if self.overlay_alpha > 0:
            overlay = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pg.SRCALPHA)
            overlay.fill((0, 0, 0, self.overlay_alpha))
            surface.blit(overlay, (0, 0))