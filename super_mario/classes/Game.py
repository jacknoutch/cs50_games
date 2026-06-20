import os, random
import pygame as pg

from super_mario.classes.Player import Player
from super_mario.classes.Tile import Tile
from super_mario.src.settings import COLOURS, TILES, FPS, TILE_SET_HEIGHT, TILE_SET_WIDTH, TILE_SIZE, VIRTUAL_HEIGHT, VIRTUAL_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH


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
        toppers_path = BASE_DIR + "tile_tops.png"

        self.tile_surface = pg.image.load(tiles_path).convert_alpha()
        self.tileset = self.load_tileset(self.tile_surface, TILE_SET_WIDTH, TILE_SET_HEIGHT)

        self.toppers_surface = pg.image.load(toppers_path).convert_alpha()
        self.toppers = self.load_tileset(self.toppers_surface, TILE_SET_WIDTH, TILE_SET_HEIGHT)


        # BACKGROUND

        self.background = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.background.fill(COLOURS.SKY_BLUE)


        # TILEMAP

        self.map_tile_width = VIRTUAL_WIDTH // TILE_SIZE
        self.map_tile_height = VIRTUAL_HEIGHT // TILE_SIZE

        self.tilemap = self.initialise_map()


        # CAMERA

        self.camera_target = 0


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

            if self.keys_pressed[pg.K_SPACE] and self.player.dy == 0:
                self.player.jump()

            if self.keys_pressed[pg.K_ESCAPE]:
                self.running = False

        self.player.update(self.dt)

        self.camera_target = self.player.frect.centerx - VIRTUAL_WIDTH / 2


    def render(self):

        # draw background onto the virtual (game) surface
        self.game_surface.blit(self.background, (0, 0))

        self.render_map(self.game_surface)

        # self.player.render(self.game_surface)
        player_pos = self.offset_camera(self.player.frect)
        self.game_surface.blit(self.player.get_surf(), player_pos)

        # scale the virtual surface to the window size and blit to the display
        scaled = pg.transform.scale(self.game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display.blit(scaled, (0, 0))

        pg.display.flip()

#--------------------------

    def load_tileset(self, tileset_surface, tiles_width: int, tiles_height: int) -> dict:

        tileset = {}

        # choose a random tileset theme
        tileset_choice = random.randint(0, 59)
        tileset_offset_x = (tileset_choice % 6) * tiles_width * TILE_SIZE
        tileset_offset_y = (tileset_choice // 6) * tiles_height * TILE_SIZE
        
        for i in range(tiles_height * tiles_width):
            x = i % tiles_width * TILE_SIZE + tileset_offset_x
            y = i // tiles_width * TILE_SIZE + tileset_offset_y
            tileset[i] = tileset_surface.subsurface((x,y), (TILE_SIZE, TILE_SIZE))

        return tileset


    def initialise_map(self):

        tilemap = []

        # fill the map with sky
        for i in range(self.map_tile_width * self.map_tile_height):
            tilemap.append(Tile(TILES.SKY, False))


        for x in range(self.map_tile_width):

            pillar_spawn = random.random() * 5 < 1 # 1/5 chance

            chasm_spawn = random.random() * 7 < 1 # 1/7 chance

            if chasm_spawn:
                continue

            for y in range(self.map_tile_height):

                tilemap_position = y * self.map_tile_width + x


                if pillar_spawn and y >= 3:
                    tilemap[tilemap_position] = Tile(TILES.GROUND, y == 3)

                elif y >= 5:
                    tilemap[tilemap_position] = Tile(TILES.GROUND, y == 5)

        return tilemap

    def render_map(self, surface):
        for i, tile in enumerate(self.tilemap):
            col = i % self.map_tile_width
            row = i // self.map_tile_width

            dest_x = int(col * TILE_SIZE - self.camera_target)
            dest_y = row * TILE_SIZE

            if dest_x + TILE_SIZE < 0 or dest_x > VIRTUAL_WIDTH:
                continue

            surface.blit(
                self.tileset[tile.id],
                (dest_x, dest_y)
            )

            if tile.topper:
                surface.blit(self.toppers[tile.id], (dest_x, dest_y))


            # print the coordinates on the screen for debug'
            if self.debug:
                coord_text = f"{col},{row}"
                text_surf = self.font.render(coord_text, True, (0, 0, 0))
                surface.blit(text_surf, (dest_x + 2, dest_y + 2))

    
    def offset_camera(self, pos):
        return (int(pos.x - self.camera_target), int(pos.y))