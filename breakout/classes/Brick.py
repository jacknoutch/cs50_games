class Brick:
    def __init__(self, surfaces, colour: str = "green", tier: int = 0):
        self.colour = colour
        self.tier = tier
        self.surfaces = surfaces
        self.rect = self.surfaces[self.colour][self.tier].get_frect()

    def update(self, dt):
        pass

    def render(self, surface):
        surface.blit(self.surfaces[self.colour][self.tier], self.rect)