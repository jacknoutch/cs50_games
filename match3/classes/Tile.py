import pygame as pg    

from match3.src.settings import TILE_SIZE
from match3.src.tween import create_pos_tween, TWEEN_DEFAULT_RATE

class Tile:

    def __init__(self, x, y, asset_manager, colour, variety=0, is_empty=False):
        
        # board position
        self.col = x
        self.row = y

        # surface and rect
        self.is_empty = is_empty
        if is_empty:
            self.surf = pg.Surface((TILE_SIZE, TILE_SIZE), pg.SRCALPHA)
            self.surf.fill((0, 0, 0, 0))
            self.rect = self.surf.get_rect()
            self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        else:
            self.surf = asset_manager.images["tiles"][colour][variety]
            self.rect = self.surf.get_frect()
            self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

        # tile properties
        self.colour = colour
        self.variety = variety

        # tweening properties
        self._is_tweening = False
        self.scale = 1.0
        self.rotation = 0.0


    def __repr__(self):
        return f"Tile(col={self.col}, row={self.row}, colour={self.colour}, variety={self.variety})"


    def start_tween(self, target_pos, duration=TWEEN_DEFAULT_RATE):
        """
        Create and return a Tween that will animate this tile.rect from its current
        position to target_pos (both in board-space pixels). The caller should add
        the returned Tween to the global TweenManager.
        """
        self._is_tweening = True

        def on_complete():
            # mark not tweening and snap rect to final position
            self._is_tweening = False
            self.rect.topleft = (int(target_pos[0]), int(target_pos[1]))

        tween = create_pos_tween(self, self.rect.topleft, target_pos, duration=duration, on_complete=on_complete)
        return tween


    def update(self, dt):

        if not self._is_tweening:
            self.rect.topleft = (self.col * TILE_SIZE, self.row * TILE_SIZE)


    def render(self, surface, offset):
        """
        Render the tile. If scale/rotation are set (from tweens), apply them to the tile image
        while keeping the tile centered at its rect center.
        """
        # capture the center to keep the transformed image aligned
        center = (self.rect.x + offset[0] + self.rect.width // 2,
                  self.rect.y + offset[1] + self.rect.height // 2)

        # start from the original surface (assume self.image exists)
        img = self.surf

        # apply scaling
        if hasattr(self, 'scale') and self.scale != 1.0:
            new_w = max(1, int(img.get_width() * self.scale))
            new_h = max(1, int(img.get_height() * self.scale))
            img = pg.transform.smoothscale(img, (new_w, new_h))

        # apply rotation
        if hasattr(self, 'rotation') and self.rotation != 0.0:
            img = pg.transform.rotate(img, self.rotation)

        # compute blit rect centered at previously computed center
        blit_rect = img.get_rect(center=center)

        # blit to surface
        surface.blit(img, blit_rect.topleft)
