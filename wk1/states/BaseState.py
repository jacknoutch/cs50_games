class BaseState:
    def enter(self, *args, **kwargs):
        pass

    def exit(self, *args, **kwargs):
        pass

    def update(self, dt):
        pass

    def render(self, *args, **kwargs):
        pass
