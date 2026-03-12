import os
import pygame as pg

class Assets:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.music = {}

        self.base_path = "assets/"

    def load_image(self, name, path):
        image = pg.image.load(path).convert_alpha()
        self.images[name] = image

    def get_image(self, name):
        return self.images.get(name)

    def load_sound(self, name, path):
        sound = pg.mixer.Sound(path)
        self.sounds[name] = sound

    def get_sound(self, name):
        return self.sounds.get(name)

    def load_music(self, name, path):
        music = pg.mixer.music.load(path)
        self.music[name] = music

    def get_music(self, name):
        return self.music.get(name)

    def load_font(self, name, path, size):
        font = pg.font.Font(path, size)
        self.fonts[name] = font

    def get_font(self, name):
        return self.fonts.get(name)
    
    def load_assets(self, base_path):
        """
        Load all assets from the specified base path.

        Images must be .png, fonts .ttf, music and sfx .wav.
        """
        try:
            # Load images
            for image_name in os.listdir(os.path.join(base_path, "images")):
                self.load_image(image_name.split(".")[0], os.path.join(base_path, "images", image_name))

            # Load sounds
            for sound_name in os.listdir(os.path.join(base_path, "sfx")):
                self.load_sound(sound_name.split(".")[0], os.path.join(base_path, "sfx", sound_name))
            
            # Load music
            for music_name in os.listdir(os.path.join(base_path, "music")):
                self.load_music(music_name.split(".")[0], os.path.join(base_path, "music", music_name))

            # Load fonts
            for font_name in os.listdir(os.path.join(base_path, "fonts")):
                self.load_font(f"small_{font_name.split('.')[0]}", os.path.join(base_path, "fonts", font_name), 8)
                self.load_font(f"medium_{font_name.split('.')[0]}", os.path.join(base_path, "fonts", font_name), 16)
                self.load_font(f"large_{font_name.split('.')[0]}", os.path.join(base_path, "fonts", font_name), 32)

        except Exception as e:
            print(f"Error loading assets: {e}")
