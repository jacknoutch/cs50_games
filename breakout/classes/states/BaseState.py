class BaseState:
    def __init__(self):
        self.state_machine = None

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        pass
