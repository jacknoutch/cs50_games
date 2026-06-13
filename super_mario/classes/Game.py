import os
import pygame as pg

from super_mario.classes.Player import Player
from super_mario.src.settings import COLOURS, TILES, FPS, TILE_SIZE, VIRTUAL_HEIGHT, VIRTUAL_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH


class Game:


    def __init__(self):
        
        pg.init()
        
        # DISPLAY

        self.display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.game_surface = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        pg.display.set_caption("Super Mario Bros")

        
        self.debug = False
        self.font = pg.font.Font(None, 12)


        self.events = None
        self.keys_pressed = None
        self.mouse_pressed = None


        # GAME ELEMENTS

        self.clock = pg.time.Clock()
        self.dt = 0


        # ASSETS

        BASE_DIR = "super_mario/assets/"
        tiles_path = BASE_DIR + "tiles.png"
        self.tile_surface = pg.image.load(tiles_path).convert_alpha()


        # BACKGROUND

        self.background = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.background.fill(COLOURS.SKY_BLUE)


        # TILEMAP

        self.map_tile_width = VIRTUAL_WIDTH // TILE_SIZE
        self.map_tile_height = VIRTUAL_HEIGHT // TILE_SIZE

        self.tilemap = []

        self.initialise_map()


        # CAMERA

        self.camera_x = 0.0
        self.camera_speed = 160.0


        # IN GAME OBJECTS

        self.player = Player()

        
        self.running = True

#-----------------------------

    def run(self):

        while self.running:

            self.dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update()
            self.render()

        pg.quit()
        os.sys.exit()


    def handle_events(self):
            
        self.keys_pressed = pg.key.get_pressed()
        self.events = []

        for event in pg.event.get():

            self.events.append(event)

            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    self.debug = not self.debug


    def update(self):

        if self.keys_pressed:

            if self.keys_pressed[pg.K_LEFT]:
                self.player.move(-1 * self.dt)
            
            if self.keys_pressed[pg.K_RIGHT]:
                self.player.move(self.dt)


        # Center camera on player
        self.camera_x = self.player.rect.x - VIRTUAL_WIDTH / 2 + self.player.tile_width / 2


    def render(self):

        # draw background onto the virtual (game) surface
        self.game_surface.blit(self.background, (0, 0))

        self.render_map(self.game_surface)

        self.player.render(self.game_surface)

        # scale the virtual surface to the window size and blit to the display
        scaled = pg.transform.scale(self.game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display.blit(scaled, (0, 0))

        pg.display.flip()

#--------------------------

    def initialise_map(self):

        for i in range(self.map_tile_width * self.map_tile_height):
            self.tilemap.append(TILES.SKY if i < self.map_tile_width * 5 else TILES.GROUND)



    def render_map(self, surface):
        tileset_cols = self.tile_surface.get_width() // TILE_SIZE

        for i, tile in enumerate(self.tilemap):
            col = i % self.map_tile_width
            row = i // self.map_tile_width

            dest_x = int(col * TILE_SIZE - self.camera_x)
            dest_y = row * TILE_SIZE

            if dest_x + TILE_SIZE < 0 or dest_x > VIRTUAL_WIDTH:
                continue

            if tile != TILES.SKY:
                src_x = (tile % tileset_cols) * TILE_SIZE
                src_y = (tile // tileset_cols) * TILE_SIZE
                surface.blit(
                    self.tile_surface,
                    (dest_x, dest_y),
                    area=pg.Rect(src_x, src_y, TILE_SIZE, TILE_SIZE),
                )


            # print the coordinates on the screen for debug'
            if self.debug:
                coord_text = f"{col},{row}"
                text_surf = self.font.render(coord_text, True, (0, 0, 0))
                surface.blit(text_surf, (dest_x + 2, dest_y + 2))
