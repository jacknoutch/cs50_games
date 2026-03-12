class StateMachine:
    def __init__(self):
        self.states = {}
        self.game = None
        self.current_state = None

    def add_state(self, name, state):
        self.states[name] = state
        self.states[name].state_machine = self

    def change_state(self, name, *args, **kwargs):
        assert name in self.states, f"State '{name}' not found"
        if self.current_state is not None:
            self.current_state.exit()
        self.current_state = self.states[name]
        self.current_state.enter(*args, **kwargs)

    def update(self):
        if self.current_state is not None:
            self.current_state.update()

    def render(self, surface):
        if self.current_state is not None:
            self.current_state.render(surface)
