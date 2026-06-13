from typing import Callable, Optional, List

TWEEN_DEFAULT_RATE = 0.3

def linear(t: float) -> float:
    return t

def ease_out_quad(t: float) -> float:
    return 1 - (1 - t) * (1 - t)

class Tween:
    def __init__(self, duration: float, update_fn: Callable[[float], None],
                 on_complete: Optional[Callable[[], None]] = None,
                 easing: Callable[[float], float] = None):
        self.duration = max(duration, 1e-6)
        self.update_fn = update_fn
        self.on_complete = on_complete
        self.easing = easing or linear
        self.elapsed = 0.0
        self.finished = False

    def update(self, dt: float):
        if self.finished:
            return
        self.elapsed += dt
        t = min(1.0, self.elapsed / self.duration)
        eased = self.easing(t)
        self.update_fn(eased)
        if t >= 1.0:
            self.finished = True
            if self.on_complete:
                self.on_complete()

class TweenManager:
    def __init__(self):
        self._tweens: List[Tween] = []

    def add(self, tween: Tween):
        self._tweens.append(tween)

    def update(self, dt: float):
        for tween in list(self._tweens):
            tween.update(dt)
            if tween.finished:
                self._tweens.remove(tween)

    def any(self) -> bool:
        return bool(self._tweens)


# helper to make a position tween for an object with a rect.topleft
def create_pos_tween(obj, start_pos, target_pos, duration=0.3,
                     on_complete=None, easing=None) -> Tween:
    sx, sy = start_pos
    tx, ty = target_pos

    def update_fn(t):
        nx = sx + (tx - sx) * t
        ny = sy + (ty - sy) * t
        obj.rect.topleft = (int(nx), int(ny))

    def finished():
        # ensure exact target
        obj.rect.topleft = (int(tx), int(ty))
        if on_complete:
            on_complete()

    return Tween(duration, update_fn, on_complete=finished, easing=easing)