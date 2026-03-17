    

from match3.src.settings import TILE_SIZE


class Tile:

    def __init__(self, x, y, asset_manager, colour, variety=0):
        
        # board position
        self.col = x
        self.row = y

        # surface and rect
        self.surf = asset_manager.images["tiles"][colour][variety]
        self.rect = self.surf.get_frect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

        # tile properties
        self.colour = colour
        self.variety = variety


    def render(self, surface, offset):

        render_x = self.rect.x + offset[0]
        render_y = self.rect.y + offset[1]
        surface.blit(self.surf, (render_x, render_y))



