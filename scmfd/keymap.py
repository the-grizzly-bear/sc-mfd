from evdev import ecodes

KEYMAP: dict[str, int] = {}
KEYMAP.update({c: getattr(ecodes, "KEY_" + c.upper()) for c in "abcdefghijklmnopqrstuvwxyz"})
KEYMAP.update({d: getattr(ecodes, "KEY_" + d) for d in "0123456789"})
KEYMAP.update({f"f{n}": getattr(ecodes, f"KEY_F{n}") for n in range(1, 25)})
KEYMAP.update({
    "altleft": ecodes.KEY_LEFTALT, "altright": ecodes.KEY_RIGHTALT,
    "shiftleft": ecodes.KEY_LEFTSHIFT, "shiftright": ecodes.KEY_RIGHTSHIFT,
    "ctrlleft": ecodes.KEY_LEFTCTRL, "ctrlright": ecodes.KEY_RIGHTCTRL,
    "capslock": ecodes.KEY_CAPSLOCK, "backspace": ecodes.KEY_BACKSPACE,
    "del": ecodes.KEY_DELETE, "tab": ecodes.KEY_TAB, "enter": ecodes.KEY_ENTER,
    "esc": ecodes.KEY_ESC, "space": ecodes.KEY_SPACE,
    "up": ecodes.KEY_UP, "down": ecodes.KEY_DOWN,
    "left": ecodes.KEY_LEFT, "right": ecodes.KEY_RIGHT,
    "-": ecodes.KEY_MINUS, "=": ecodes.KEY_EQUAL,
    "[": ecodes.KEY_LEFTBRACE, "]": ecodes.KEY_RIGHTBRACE, "\\": ecodes.KEY_BACKSLASH,
    ";": ecodes.KEY_SEMICOLON, "'": ecodes.KEY_APOSTROPHE, "`": ecodes.KEY_GRAVE,
    ",": ecodes.KEY_COMMA, ".": ecodes.KEY_DOT, "/": ecodes.KEY_SLASH,
    "mouseleft": ecodes.BTN_LEFT, "mouseright": ecodes.BTN_RIGHT, "mousemiddle": ecodes.BTN_MIDDLE,
})


def code(name: str) -> int | None:
    return KEYMAP.get(name.lower())
