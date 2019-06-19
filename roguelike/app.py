#!/usr/bin/env python3
"""
app.py

Roguelike Game
"""
from os import path

import tcod
import tcod.event

from .components.fighter import Fighter
from .death_functions import kill_monster, kill_player
from .entity import Entity, get_blocking_entities_at_location
from .fov_functions import initialize_fov, recompute_fov
from .game_messages import MessageLog
from .game_states import GameStates
from .input_handlers import handle_keys
from .map_objects.game_map import GameMap
from .render_functions import RenderOrder, clear_all, render_all

TITLE = "roguelike tutorial"
FONT_IMAGE = "arial10x10.png"
HERE = path.abspath(path.dirname(__file__))
CUSTOM_FONT = f"{HERE}/resources/{FONT_IMAGE}"
FULL_SCREEN = False

PLAYER_BG = tcod.BKGND_NONE
MAP_WIDTH = 80
MAP_HEIGHT = 43
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

MESSAGE_X = BAR_WIDTH + 2
MESSAGE_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MESSAGE_HEIGHT = PANEL_HEIGHT - 1

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

FOV_ALGORITHM = 0
FOV_LIGHT_WALLS = True
FOV_RADIUS = 10

MAX_MONSTERS_PER_ROOM = 3
MAX_ITEMS_PER_ROOM = 2
COLORS = {
    "dark_wall": tcod.Color(0, 0, 100),
    "dark_ground": tcod.Color(50, 50, 150),
    "light_wall": tcod.Color(130, 110, 50),
    "light_ground": tcod.Color(200, 180, 50),
}


def main():
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(
        0,
        0,
        "@",
        tcod.white,
        "Player",
        blocks=True,
        render_order=RenderOrder.ACTOR,
        fighter=fighter_component,
    )
    entities = [player]

    tcod.console_set_custom_font(
        CUSTOM_FONT, tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_TCOD
    )

    with tcod.console_init_root(
        SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FULL_SCREEN, tcod.RENDERER_SDL2, "F", True
    ) as con:
        panel = tcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
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
            MAX_ITEMS_PER_ROOM,
        )
        fov_recompute = True
        fov_map = initialize_fov(game_map)
        message_log = MessageLog(MESSAGE_X, MESSAGE_WIDTH, MESSAGE_HEIGHT)

        while not tcod.console_is_window_closed():
            tcod.sys_check_for_event(
                tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse
            )

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
                panel,
                entities,
                player,
                game_map,
                fov_map,
                fov_recompute,
                message_log,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                BAR_WIDTH,
                PANEL_HEIGHT,
                PANEL_Y,
                mouse,
                COLORS,
            )
            fov_recompute = False
            tcod.console_flush()
            clear_all(con, entities)
            action = handle_keys(key)
            move = action.get("move")
            exit_game = action.get("exit")
            full_screen = action.get("full_screen")
            player_turn_results = []

            if move and game_state == GameStates.PLAYERS_TURN:
                dx, dy = move
                destination_x = player.x + dx
                destination_y = player.y + dy

                if not game_map.is_blocked(destination_x, destination_y):
                    target = get_blocking_entities_at_location(
                        entities, destination_x, destination_y
                    )

                    if target:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)
                    else:
                        player.move(dx, dy)
                        fov_recompute = True

                    game_state = GameStates.ENEMY_TURN

            if exit_game:
                return True

            if full_screen:
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

            for player_turn_result in player_turn_results:
                message = player_turn_result.get("message")
                dead_entity = player_turn_result.get("dead")

                if message:
                    message_log.add_message(message)

                if dead_entity:
                    if dead_entity == player:
                        message, game_state = kill_player(dead_entity)
                    else:
                        message = kill_monster(dead_entity)

                    message_log.add_message(message)

            if game_state == GameStates.ENEMY_TURN:
                for entity in entities:
                    if entity.ai:
                        enemy_turn_results = entity.ai.take_turn(
                            player, fov_map, game_map, entities
                        )

                        for enemy_turn_result in enemy_turn_results:
                            message = enemy_turn_result.get("message")
                            dead_entity = enemy_turn_result.get("dead")

                            if message:
                                message_log.add_message(message)

                            if dead_entity:
                                if dead_entity == player:
                                    message, game_state = kill_player(dead_entity)
                                else:
                                    message = kill_monster(dead_entity)

                                message_log.add_message(message)

                                if game_state == GameStates.PLAYER_DEAD:
                                    break

                        if game_state == GameStates.PLAYER_DEAD:
                            break

                else:
                    game_state = GameStates.PLAYERS_TURN


if __name__ == "__main__":
    main()
