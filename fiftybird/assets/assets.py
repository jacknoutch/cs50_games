import pygame as pg
from fiftybird.settings import PIPE_IMAGE, BIRD_IMAGE, BACKGROUND_IMAGE, GROUND_IMAGE

def load_assets():
    # must be called after pg.display.set_mode(...)

    ## Images
    global pipe, bird, background, ground
    pipe = pg.image.load(PIPE_IMAGE).convert_alpha()
    bird = pg.image.load(BIRD_IMAGE).convert_alpha()
    background = pg.image.load(BACKGROUND_IMAGE).convert()
    ground = pg.image.load(GROUND_IMAGE).convert()

    ## Fonts
    global small_font, medium_font, flappy_font, huge_font
    small_font = pg.font.Font("wk1/assets/font.ttf", 8)
    medium_font = pg.font.Font("wk1/assets/font.ttf", 14)
    flappy_font = pg.font.Font("wk1/assets/font.ttf", 28)
    huge_font = pg.font.Font("wk1/assets/font.ttf", 56)

    # Sounds
    global explosion_sound, jump_sound, hurt_sound, score_sound
    explosion_sound = pg.mixer.Sound("wk1/assets/sfx/explosion.wav")
    jump_sound = pg.mixer.Sound("wk1/assets/sfx/jump.wav")
    hurt_sound = pg.mixer.Sound("wk1/assets/sfx/hurt.wav")
    score_sound = pg.mixer.Sound("wk1/assets/sfx/score.wav")

    # Music
    global main_music
    main_music = pg.mixer.Sound("wk1/assets/music/marios_way.mp3")