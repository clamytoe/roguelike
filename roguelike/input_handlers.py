import tcod

TCOD_KEYS = {
    tcod.KEY_UP: {"move": (0, -1)},
    tcod.KEY_DOWN: {"move": (0, 1)},
    tcod.KEY_LEFT: {"move": (-1, 0)},
    tcod.KEY_RIGHT: {"move": (1, 0)},
    tcod.KEY_ESCAPE: {"exit": True},
}
KB_KEYS = {
    "k": {"move": (0, -1)},
    "j": {"move": (0, 1)},
    "h": {"move": (-1, 0)},
    "l": {"move": (1, 0)},
    "y": {"move": (-1, -1)},
    "u": {"move": (1, -1)},
    "b": {"move": (-1, 1)},
    "n": {"move": (1, 1)},
    "g": {"pickup": True},
}


def handle_keys(key):
    key_char = chr(key.c)

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {"full_screen": True}
    elif key_char in KB_KEYS:
        return KB_KEYS[key_char]
    else:
        return TCOD_KEYS.get(key.vk, {})
