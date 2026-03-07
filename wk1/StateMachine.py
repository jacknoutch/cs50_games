import pygame as pg

from wk1.states.BaseState import BaseState

class StateMachine:
    def __init__(self, states: dict | None = None):
        self.base = BaseState()
        self.states = states if states is not None else {}
        self.current_state = self.base

    def change_state(self, new_state):
        assert new_state in self.states, f"State {new_state} does not exist in the state machine."
        self.current_state.exit()

        factory = self.states[new_state]

        if callable(factory):
            state_object = factory()
        else:
            state_object = factory

        state_object.state_machine = self

        self.current_state = state_object
        self.current_state.enter()

    def update(self, dt, keys_pressed: pg.key.ScancodeWrapper):
        self.current_state.update(dt, keys_pressed=keys_pressed)

    def render(self, *args, **kwargs):
        self.current_state.render(*args, **kwargs)
