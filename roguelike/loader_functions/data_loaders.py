import os
import shelve
import shutil

from roguelike.fov_functions import initialize_fov
from roguelike.game_states import GameStates

FILE_NAME = "save_game"
HERE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
GAME_FILE = os.path.join(HERE, FILE_NAME)


def save_game(player, entities, game_map, message_log, game_state):
    with shelve.open(GAME_FILE, "c") as data_file:
        data_file["player"] = player
        data_file["entities"] = [e for e in entities if e is not player]
        data_file["game_map"] = game_map
        data_file["message_log"] = message_log
        data_file["game_state"] = game_state

    # Create backup AFTER saving the cleaned, correct state
    save_path = GAME_FILE + ".dat"
    backup_path = GAME_FILE + ".bak"
    shutil.copy(save_path, backup_path)


def load_game():
    try:
        with shelve.open(GAME_FILE, "r") as data_file:
            player = data_file["player"]
            entities = data_file["entities"]
            game_map = data_file["game_map"]
            message_log = data_file["message_log"]
            game_state = data_file["game_state"]
    except:
        raise FileNotFoundError("Save file not found")

    if game_state == GameStates.PLAYER_DEAD:
        raise FileNotFoundError("Save file is invalid (player is dead)")

    # Rebind owners
    player.__post_init__()
    for e in entities:
        e.__post_init__()

    entities.insert(0, player)

    return player, entities, game_map, message_log, game_state

