import tcod

from .game_states import GameStates

ESCAPE = {"exit": True}
FULL_SCREEN = {"full_screen": True}
INVENTORY = {"show_inventory": True}
TCOD_KEYS = {
    tcod.KEY_UP: {"move": (0, -1)},
    tcod.KEY_DOWN: {"move": (0, 1)},
    tcod.KEY_LEFT: {"move": (-1, 0)},
    tcod.KEY_RIGHT: {"move": (1, 0)},
    tcod.KEY_ENTER: {"take_stairs": True},
    tcod.KEY_ESCAPE: ESCAPE,
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
    "d": {"drop_inventory": True},
    "c": {"show_character_screen": True},
    "z": {"wait": True},
    "i": INVENTORY,
}


def handle_keys(key, game_state):
    func = GAME_STATES.get(game_state, {})

    return func(key) if func else func


def handle_inventory_keys(key):
    index = key.c - ord("a")

    if index >= 0:
        return {"inventory_index": index}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return FULL_SCREEN
    elif key.vk == tcod.KEY_ESCAPE:
        return ESCAPE

    return {}


def handle_player_turn_keys(key):
    key_char = chr(key.c)

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return FULL_SCREEN
    elif key_char in KB_KEYS.keys():
        return KB_KEYS[key_char]
    else:
        return TCOD_KEYS.get(key.vk, {})


def handle_targeting_keys(key):
    if key.vk == tcod.KEY_ESCAPE:
        return ESCAPE

    return {}


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == "i":
        return INVENTORY

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return FULL_SCREEN
    elif key.vk == tcod.KEY_ESCAPE:
        return ESCAPE

    return {}


def handle_main_menu(key):
    if key.vk == tcod.KEY_ESCAPE:
        return ESCAPE

    menu_keys = {"a": {"new_game": True}, "b": {"load_game": True}, "c": ESCAPE}

    return menu_keys.get(chr(key.c), {})


def handle_level_up_menu(key):
    level_up_keys = {
        "a": {"level_up": "hp"},
        "b": {"level_up": "str"},
        "c": {"level_up": "def"},
    }

    return level_up_keys.get(chr(key.c), {})


def handle_character_screen(key):
    return ESCAPE if key.vk == tcod.KEY_ESCAPE or chr(key.c) == "c" else {}


def handle_mouse(mouse):
    x, y = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {"left_click": (x, y)}
    elif mouse.rbutton_pressed:
        return {"right_click": (x, y)}

    return {}


GAME_STATES = {
    GameStates.PLAYERS_TURN: handle_player_turn_keys,
    GameStates.PLAYER_DEAD: handle_player_dead_keys,
    GameStates.TARGETING: handle_targeting_keys,
    GameStates.LEVEL_UP: handle_level_up_menu,
    GameStates.CHARACTER_SCREEN: handle_character_screen,
    GameStates.SHOW_INVENTORY: handle_inventory_keys,
    GameStates.DROP_INVENTORY: handle_inventory_keys,
}
