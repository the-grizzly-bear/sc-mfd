import time
from evdev import UInput, AbsInfo, ecodes

from .keymap import KEYMAP, code
from .model import Command

_POINTER = {ecodes.BTN_LEFT, ecodes.BTN_RIGHT, ecodes.BTN_MIDDLE}


class VirtualKeyboard:
    def __init__(self, name: str = "scmfd") -> None:
        keys = sorted(set(KEYMAP.values()) - _POINTER)
        self._kbd = UInput({ecodes.EV_KEY: keys}, name=name)
        self._aux = UInput({ecodes.EV_KEY: [ecodes.BTN_TRIGGER, *_POINTER],
                            ecodes.EV_ABS: [(ecodes.ABS_X, AbsInfo(0, -32767, 32767, 0, 0, 0))]},
                           name=f"{name}-stick")
        time.sleep(0.5)

    def run(self, commands: list[Command]) -> None:
        for c in commands:
            kind, value = c.get("type"), c.get("value", "")
            if kind == "delay":
                time.sleep(int(value) / 1000)
            elif kind == "axis":
                self._aux.write(ecodes.EV_ABS, ecodes.ABS_X, round(float(value) * 32767))
                self._aux.syn()
            elif (key := code(value)) is not None:
                mod = code(c["modifier"]) if c.get("modifier") else None
                if kind in ("down", "press"):
                    if mod:
                        self._emit(mod, 1)
                    self._emit(key, 1)
                if kind == "press":
                    time.sleep(0.02)
                if kind in ("up", "press"):
                    self._emit(key, 0)
                    if mod:
                        self._emit(mod, 0)

    def _emit(self, key: int, value: int) -> None:
        dev = self._aux if key in _POINTER else self._kbd
        dev.write(ecodes.EV_KEY, key, value)
        dev.syn()

    def close(self) -> None:
        self._kbd.close()
        self._aux.close()

    def __enter__(self) -> "VirtualKeyboard":
        return self

    def __exit__(self, *exc) -> None:
        self.close()
