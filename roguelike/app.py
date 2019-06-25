#!/usr/bin/env python3
"""
app.py

Roguelike Game
"""
from os import path

import tcod
import tcod.event

from .death_functions import kill_monster, kill_player
from .entity import get_blocking_entities_at_location
from .fov_functions import initialize_fov, recompute_fov
from .game_messages import Message
from .game_states import GameStates
from .input_handlers import handle_keys, handle_mouse
from .loader_functions.initialize_new_game import get_constants, get_game_variables
from .render_functions import clear_all, render_all

FONT_IMAGE = "arial10x10.png"
HERE = path.abspath(path.dirname(__file__))
CUSTOM_FONT = f"{HERE}/resources/{FONT_IMAGE}"


def main():
    constants = get_constants()

    tcod.console_set_custom_font(
        CUSTOM_FONT, tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_TCOD
    )

    tcod.console_init_root(
        constants["screen_width"],
        constants["screen_height"],
        constants["window_title"],
        constants["full_screen"],
        constants["renderer"],
        "F",
        True,
    )
    con = tcod.console_new(constants["screen_width"], constants["screen_height"])
    panel = tcod.console_new(constants["screen_width"], constants["panel_height"])

    player, entities, game_map, message_log, game_state = get_game_variables(constants)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()

    previous_game_state = game_state
    targeting_item = None

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(
                fov_map,
                player.x,
                player.y,
                constants["fov_radius"],
                constants["fov_light_walls"],
                constants["fov_algorithm"],
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
            constants["screen_width"],
            constants["screen_height"],
            constants["bar_width"],
            constants["panel_height"],
            constants["panel_y"],
            mouse,
            constants["colors"],
            game_state,
        )

        fov_recompute = False
        tcod.console_flush()
        clear_all(con, entities)

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get("move")
        pickup = action.get("pickup")
        show_inventory = action.get("show_inventory")
        drop_inventory = action.get("drop_inventory")
        inventory_index = action.get("inventory_index")
        exit_game = action.get("exit")
        full_screen = action.get("full_screen")

        left_click = mouse_action.get("left_click")
        right_click = mouse_action.get("right_click")

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
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    break
            else:
                message_log.add_message(
                    Message("There is nothing here to pick up.", tcod.yellow)
                )

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if (
            inventory_index is not None
            and previous_game_state != GameStates.PLAYER_DEAD
            and inventory_index < len(player.inventory.items)
        ):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(
                    player.inventory.use(item, entities=entities, fov_map=fov_map)
                )
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click
                item_use_results = player.inventory.use(
                    targeting_item,
                    entities=entities,
                    fov_map=fov_map,
                    target_x=target_x,
                    target_y=target_y,
                )
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({"targeting_cancelled": True})

        if exit_game:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({"targeting_cancelled": True})
            else:
                return True

        if full_screen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get("message")
            dead_entity = player_turn_result.get("dead")
            item_added = player_turn_result.get("item_added")
            item_consumed = player_turn_result.get("consumed")
            item_dropped = player_turn_result.get("item_dropped")
            targeting = player_turn_result.get("targeting")
            targeting_cancelled = player_turn_result.get("targeting_cancelled")

            if message:
                message_log.add_message(message)

            if targeting_cancelled:
                game_state = previous_game_state
                message_log.add_message(Message("Targeting cancelled"))

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

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
