import pygame as pg

BASE_DIR = "match3/assets"
TILE_SIZE = 32
TILE_ROW_COUNT = 9
TILE_COLUMN_COUNT = 12

# Asset paths
ASSET_PATHS = {
    "images": {
        "background": f"{BASE_DIR}/images/background.png",
        "tiles": f"{BASE_DIR}/images/match3.png",
    },
    "sfx": {
        "clock": f"{BASE_DIR}/sfx/clock.wav",
        "error": f"{BASE_DIR}/sfx/error.wav",
        "game-over": f"{BASE_DIR}/sfx/game-over.wav",
        "match": f"{BASE_DIR}/sfx/match.wav",
        "next-level": f"{BASE_DIR}/sfx/next-level.wav",
        "select": f"{BASE_DIR}/sfx/select.wav",
    },
    "fonts": {
        "font": f"{BASE_DIR}/fonts/font.ttf",
    },
    "music": {
        "music1": f"{BASE_DIR}/music/music.mp3",
        "music2": f"{BASE_DIR}/music/music2.mp3",
        "music3": f"{BASE_DIR}/music/music3.mp3",
    }
}

class AssetManager:

    def __init__(self):
        self.images = {}
        self.sfx = {}
        self.fonts = {}
        self.music = {}

    def load_image(self, name, path):
        image = pg.image.load(path).convert_alpha()
        self.images[name] = image

    def get_image(self, name):
        return self.images.get(name)

    def parse_tiles(self):
        """
        Parse a sprite sheet into individual tiles, resulting in a 2d array of surfaces.
        """
        tiles_image = self.images.get("tiles")
        if not tiles_image:
            return

        tile_width = TILE_SIZE
        tile_height = TILE_SIZE
        columns = TILE_COLUMN_COUNT
        rows = TILE_ROW_COUNT

        tiles = []

        for row in range(rows):
            row_tiles = []
            for col in range(columns):
                tile = tiles_image.subsurface((col * tile_width, row * tile_height, tile_width, tile_height))
                row_tiles.append(tile)
            tiles.append(row_tiles)

        self.images["tiles"] = tiles

    def load_sfx(self, name, path):
        sound = pg.mixer.Sound(path)
        self.sfx[name] = sound

    def get_sfx(self, name):
        return self.sfx.get(name)

    def load_font(self, name, path, sizes=[12, 24, 36]):
        for size in sizes:
            font = pg.font.Font(path, size)
            self.fonts[(name, size)] = font

    def get_font(self, name, size):
        return self.fonts.get((name, size))

    def load_music(self, path, name):
        self.music[name] = path

    def play_music(self, name, loop=-1):
        pg.mixer.music.load(self.music[name])
        pg.mixer.music.play(loop)

    def stop_music(self):
        pg.mixer.music.stop()

    def load_assets(self):
        for category, assets in ASSET_PATHS.items():
            for name, path in assets.items():
                if category == "images":
                    self.load_image(name, path)
                elif category == "sfx":
                    self.load_sfx(name, path)
                elif category == "fonts":
                    self.load_font(name, path)
                elif category == "music":
                    self.load_music(path, name)

        self.parse_tiles()