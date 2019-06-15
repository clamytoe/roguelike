#!/usr/bin/env python3
"""
app.py

Roguelike Game
"""
from os import path

import tcod
import tcod.event

from .components.fighter import Fighter
from .entity import Entity, get_blocking_entities_at_location
from .fov_functions import initialize_fov, recompute_fov
from .game_states import GameStates
from .input_handlers import handle_keys
from .map_objects.game_map import GameMap
from .render_functions import clear_all, clear_entity, draw_entity, render_all

TITLE = "roguelike tutorial"
FONT_IMAGE = "arial10x10.png"
HERE = path.abspath(path.dirname(__file__))
CUSTOM_FONT = f"{HERE}/resources/{FONT_IMAGE}"
FULL_SCREEN = False
PLAYER_BG = tcod.BKGND_NONE
MAP_WIDTH = 80
MAP_HEIGHT = 45
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
FOV_ALGORITHM = 0
FOV_LIGHT_WALLS = True
FOV_RADIUS = 10
MAX_MONSTERS_PER_ROOM = 3
COLORS = {
    "dark_wall": tcod.Color(0, 0, 100),
    "dark_ground": tcod.Color(50, 50, 150),
    "light_wall": tcod.Color(130, 110, 50),
    "light_ground": tcod.Color(200, 180, 50),
}


def main():
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, "@", tcod.white, "Player", blocks=True, fighter=fighter_component)
    entities = [player]

    tcod.console_set_custom_font(
        CUSTOM_FONT, tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_TCOD
    )

    with tcod.console_init_root(
        SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FULL_SCREEN, tcod.RENDERER_SDL2, "F", True
    ) as con:
        key = tcod.Key()
        mouse = tcod.Mouse()
        game_state = GameStates.PLAYERS_TURN
        game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
        game_map.make_map(
            MAX_ROOMS,
            ROOM_MIN_SIZE,
            ROOM_MAX_SIZE,
            MAP_WIDTH,
            MAP_HEIGHT,
            player,
            entities,
            MAX_MONSTERS_PER_ROOM,
        )
        fov_recompute = True
        fov_map = initialize_fov(game_map)

        while not tcod.console_is_window_closed():
            tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

            if fov_recompute:
                recompute_fov(
                    fov_map,
                    player.x,
                    player.y,
                    FOV_RADIUS,
                    FOV_LIGHT_WALLS,
                    FOV_ALGORITHM,
                )

            render_all(
                con,
                entities,
                game_map,
                fov_map,
                fov_recompute,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                COLORS,
            )
            fov_recompute = False
            tcod.console_flush()
            clear_all(con, entities)
            action = handle_keys(key)
            move = action.get("move")
            exit_game = action.get("exit")
            full_screen = action.get("full_screen")

            if move and game_state == GameStates.PLAYERS_TURN:
                dx, dy = move
                destination_x = player.x + dx
                destination_y = player.y + dy

                if not game_map.is_blocked(destination_x, destination_y):
                    target = get_blocking_entities_at_location(
                        entities, destination_x, destination_y
                    )

                    if target:
                        print(
                            f"You kick the {target.name} in the shins, much to its annoyance!"
                        )
                    else:
                        player.move(dx, dy)
                        fov_recompute = True

                    game_state = GameStates.ENEMY_TURN

            if exit_game:
                return True

            if full_screen:
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

            if game_state == GameStates.ENEMY_TURN:
                for entity in entities:
                    if entity.ai:
                        entity.ai.take_turn(player, fov_map, game_map, entities)

                game_state = GameStates.PLAYERS_TURN


if __name__ == "__main__":
    main()
