from tcod import libtcodpy

from .game_states import GameStates

ESCAPE = {"exit": True}
FULL_SCREEN = {"full_screen": True}
INVENTORY = {"show_inventory": True}
TCOD_KEYS = {
    libtcodpy.KEY_UP: {"move": (0, -1)},
    libtcodpy.KEY_DOWN: {"move": (0, 1)},
    libtcodpy.KEY_LEFT: {"move": (-1, 0)},
    libtcodpy.KEY_RIGHT: {"move": (1, 0)},
    libtcodpy.KEY_END: {"take_stairs": True},
    libtcodpy.KEY_ESCAPE: ESCAPE,

    # Numpad movement (8 directions)
    libtcodpy.KEY_KP8: {"move": (0, -1)},     # up
    libtcodpy.KEY_KP2: {"move": (0, 1)},      # down
    libtcodpy.KEY_KP4: {"move": (-1, 0)},     # left
    libtcodpy.KEY_KP6: {"move": (1, 0)},      # right

    libtcodpy.KEY_KP7: {"move": (-1, -1)},    # up-left
    libtcodpy.KEY_KP9: {"move": (1, -1)},     # up-right
    libtcodpy.KEY_KP1: {"move": (-1, 1)},     # down-left
    libtcodpy.KEY_KP3: {"move": (1, 1)},      # down-right

    # Optional: ENTER = wait
    libtcodpy.KEY_ENTER: {"wait": True},
}
KB_KEYS = {
    # Vi-style movement (already present)
    "k": {"move": (0, -1)},
    "j": {"move": (0, 1)},
    "h": {"move": (-1, 0)},
    "l": {"move": (1, 0)},
    "y": {"move": (-1, -1)},
    "u": {"move": (1, -1)},
    "b": {"move": (-1, 1)},
    "n": {"move": (1, 1)},

    # WASD movement
    "w": {"move": (0, -1)},     # up
    "s": {"move": (0, 1)},      # down
    "a": {"move": (-1, 0)},     # left
    "d": {"move": (1, 0)},      # right

    # QEZC diagonals (roguelike standard)
    "q": {"move": (-1, -1)},    # up-left
    "e": {"move": (1, -1)},     # up-right
    "z": {"move": (-1, 1)},     # down-left
    "c": {"move": (1, 1)},      # down-right

    # Actions
    "g": {"pickup": True},
    "x": {"drop_inventory": True},
    "p": {"show_character_screen": True},
    "i": INVENTORY,
}


def handle_keys(key, game_state):
    func = GAME_STATES.get(game_state, {})

    if callable(func):
        return func(key)
    
    return func


def handle_inventory_keys(key):
    index = key.c - ord("a")

    if index >= 0:
        return {"inventory_index": index}

    if key.vk == libtcodpy.KEY_ENTER and key.lalt:
        return FULL_SCREEN
    elif key.vk == libtcodpy.KEY_ESCAPE:
        return ESCAPE

    return {}


def handle_player_turn_keys(key):
    key_char = chr(key.c)

    # Fullscreen toggle
    if key.vk == libtcodpy.KEY_ENTER and key.lalt:
        return FULL_SCREEN

    # Wait (ENTER without ALT)
    if key.vk == libtcodpy.KEY_ENTER:
        return {"wait": True}

    # WASD / QEZC / vi keys
    if key_char in KB_KEYS:
        return KB_KEYS[key_char]

    # Arrow keys / numpad
    return TCOD_KEYS.get(key.vk, {})


def handle_targeting_keys(key):
    if key.vk == libtcodpy.KEY_ESCAPE:
        return ESCAPE

    return {}


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == "i":
        return INVENTORY

    if key.vk == libtcodpy.KEY_ENTER and key.lalt:
        return FULL_SCREEN
    elif key.vk == libtcodpy.KEY_ESCAPE:
        return ESCAPE

    return {}


def handle_main_menu(key):
    if key.vk == libtcodpy.KEY_ESCAPE:
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
    return ESCAPE if key.vk == libtcodpy.KEY_ESCAPE or chr(key.c) == "c" else {}


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
