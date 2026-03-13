from match3.src.utils import debug


class BaseState:
    def __init__(self):
        self.state_machine = None

    def enter(self):
        self.game = self.state_machine.game
        if self.game.debug:
            print("Entered state: " + self.__class__.__name__)

    def exit(self):
        if self.game.debug:
            print("Exited state: " + self.__class__.__name__)

    def update(self, dt):
        pass

    def render(self, surface):
        pass
