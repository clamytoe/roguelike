import tcod

from .game_states import GameStates

EXIT_GAME = {"exit": True}
FULL_SCREEN = {"full_screen": True}
INVENTORY = {"show_inventory": True}
TCOD_KEYS = {
    tcod.KEY_UP: {"move": (0, -1)},
    tcod.KEY_DOWN: {"move": (0, 1)},
    tcod.KEY_LEFT: {"move": (-1, 0)},
    tcod.KEY_RIGHT: {"move": (1, 0)},
    tcod.KEY_ESCAPE: EXIT_GAME,
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
    "i": INVENTORY,
}


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    return {}


def handle_inventory_keys(key):
    index = key.c - ord("a")

    if index >= 0:
        return {"inventory_index": index}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return FULL_SCREEN
    elif key.vk == tcod.KEY_ESCAPE:
        return EXIT_GAME

    return {}


def handle_player_turn_keys(key):
    key_char = chr(key.c)

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return FULL_SCREEN
    elif key_char in KB_KEYS.keys():
        return KB_KEYS[key_char]
    else:
        return TCOD_KEYS.get(key.vk, {})


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == "i":
        return INVENTORY

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return FULL_SCREEN
    elif key.vk == tcod.KEY_ESCAPE:
        return EXIT_GAME

    return {}
