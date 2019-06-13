import tcod

KEYS = {
    tcod.KEY_UP: {"move": (0, -1)},
    tcod.KEY_DOWN: {"move": (0, 1)},
    tcod.KEY_LEFT: {"move": (-1, 0)},
    tcod.KEY_RIGHT: {"move": (1, 0)},
    tcod.KEY_ESCAPE: {"exit": True},
}


def handle_keys(key):
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {"fullscreen": True}
    else:
        return KEYS.get(key.vk, {})
