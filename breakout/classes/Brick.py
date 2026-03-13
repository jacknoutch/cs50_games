BRICK_COLOURS = ["blue", "green", "red", "purple", "yellow", "grey"]

class Brick:
    def __init__(self, surfaces, colour: str = "red", tier: int = 0):
        self.colour = colour
        self.colour_index = BRICK_COLOURS.index(colour)
        self.tier = tier
        self.surfaces = surfaces
        self.rect = self.surfaces[self.colour][self.tier].get_frect()
        self.inplay = True

    def update(self, dt):
        pass

    def update_hit(self):
        self.colour_index = (self.colour_index - 1)

        if self.colour_index < 0:
            self.colour_index = 0
            self.inplay = False
        else:
            self.colour = BRICK_COLOURS[self.colour_index]

    def render(self, surface):
        surface.blit(self.surfaces[self.colour][self.tier], self.rect)

    def calculate_score(self):
        base_score = 100
        return (BRICK_COLOURS.index(self.colour) + 1) * (self.tier + 1) * base_score