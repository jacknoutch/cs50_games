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
    

class ShrinkSpinTween:
    """
    This Tween simultaneously spins an object 180 degrees and shrinks it to its center.
    
    The object must have attributes "scale" and "rotation.

    """
    
    def __init__(self, obj, duration, on_complete, easing):
        self.obj = obj
        self.duration = duration
        self.on_complete = on_complete
        self.easing = easing

        self.elapsed = 0.0
        self.start_w = obj.rect.width
        self.start_h = obj.rect.height

        # ensure obj has scale/rotation properties used by obj.render
        assert(hasattr(obj, "scale"))
        assert(hasattr(obj, "rotation"))
        
        self.center = obj.rect.center
        self.finished = False

    def update(self, dt):
        if self.finished:
            return

        self.elapsed += dt
        t = min(1.0, self.elapsed / self.duration)
        eased = self.easing(t)

        # scale goes from 1.0 -> 0.0, rotation from 0 -> 360
        new_scale = max(0.0, 1.0 - eased)
        new_rotation = eased * 180.0

        # apply to obj (obj.render should respect these)
        self.obj.scale = new_scale
        self.obj.rotation = new_rotation

        # also keep rect sized to scaled dimensions so other logic / collision works
        new_w = max(0, int(self.start_w * new_scale))
        new_h = max(0, int(self.start_h * new_scale))

        cx, cy = self.center
        # when size becomes 0 we still want rect centered at same point
        if new_w == 0: new_w = 1
        if new_h == 0: new_h = 1

        self.obj.rect.width = new_w
        self.obj.rect.height = new_h
        self.obj.rect.topleft = (cx - new_w // 2, cy - new_h // 2)

        if t >= 1.0:
            self.finished = True
            # reset visual properties to defaults before replacing obj
            self.obj.scale = 1.0
            self.obj.rotation = 0.0
            if self.on_complete:
                self.on_complete()


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