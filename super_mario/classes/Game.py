import os
import pygame as pg

from super_mario.src.settings import COLOURS, TILES, FPS, TILE_HEIGHT, TILE_WIDTH, VIRTUAL_HEIGHT, VIRTUAL_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH


class Game:


    def __init__(self):
        
        pg.init()
        
        # DISPLAY

        self.display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.game_surface = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        pg.display.set_caption("Super Mario Bros")

        
        self.debug = True


        self.events = None
        self.keys_pressed = None
        self.mouse_pressed = None


        # GAME ELEMENTS

        self.clock = pg.time.Clock()
        self.dt = 0

        BASE_DIR = "super_mario/assets/"
        tiles_path = BASE_DIR + "tiles.png"

        self.tile_surface = pg.image.load(tiles_path).convert_alpha()

        self.background = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.background.fill(COLOURS.SKY_BLUE)

        self.map_tile_width = VIRTUAL_WIDTH // TILE_WIDTH
        self.map_tile_height = VIRTUAL_HEIGHT // TILE_HEIGHT

        self.tilemap = []

        self.initialise_map()
        
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

                if event.key == pg.K_d:
                    self.debug = not self.debug


    def update(self):

        pass


    def render(self):

        # draw background onto the virtual (game) surface
        self.game_surface.blit(self.background, (0, 0))

        self.render_map(self.game_surface)

        # scale the virtual surface to the window size and blit to the display
        scaled = pg.transform.scale(self.game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display.blit(scaled, (0, 0))

        pg.display.flip()

#--------------------------

    def initialise_map(self):

        for i in range(self.map_tile_width * self.map_tile_height):
            self.tilemap.append(TILES.SKY if i < self.map_tile_width * 5 else TILES.GROUND)


    def render_map(self, surface):
        # number of tiles per row in the tileset image
        for i, tile in enumerate(self.tilemap):
            if tile == TILES.SKY:
                continue

            # destination position on the map (map index -> x,y)
            dest_x = (i % self.map_tile_width) * TILE_WIDTH
            dest_y = (i // self.map_tile_width) * TILE_HEIGHT

            surface.blit(
                self.tile_surface,
                (dest_x, dest_y),
            )