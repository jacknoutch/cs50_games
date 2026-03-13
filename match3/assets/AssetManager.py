import pygame as pg

# Asset paths
ASSET_PATHS = {
    "images": {
        "background": "assets/images/background.png",
        "tiles": "assets/images/match3.png",
    },
    "sfx": {
        "clock": "assets/sfx/clock.wav",
        "error": "assets/sfx/error.wav",
        "game-over": "assets/sfx/game-over.wav",
        "match": "assets/sfx/match.wav",
        "next-level": "assets/sfx/next-level.wav",
        "select": "assets/sfx/select.wav",
    },
    "fonts": {
        "font": "assets/fonts/font.ttf",
    },
    "music": {
        "1": "assets/music/music.mp3",
        "2": "assets/music/music2.mp3",
        "3": "assets/music/music3.mp3",
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
        music = pg.mixer.music.load(path)
        self.music[name] = music

    def play_music(self, loop=-1):
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