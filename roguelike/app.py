#!/usr/bin/env python3
"""
app.py — Main game loop and application entry point.
"""

from __future__ import annotations

import random
import os, shutil
from os import path
from typing import List, Optional

import tcod
from tcod import libtcodpy

from .colors import Colors
from .death_functions import kill_monster, kill_player
from .entity import Entity, get_blocking_entities_at_location
from .fov_functions import initialize_fov, recompute_fov
from .game_messages import Message
from .game_states import GameStates
from .input_handlers import handle_keys, handle_main_menu, handle_mouse
from .loader_functions.data_loaders import load_game, save_game, GAME_FILE
from .loader_functions.initialize_new_game import get_constants, get_game_variables
from .menus import main_menu, message_box
from .render_functions import clear_all, render_all

MENU_IMAGE = "menu_background1.png"
FONT_IMAGE = "arial10x10.png"

HERE = path.abspath(path.dirname(__file__))
MENU_BACKGROUND = f"{HERE}/resources/{MENU_IMAGE}"
CUSTOM_FONT = f"{HERE}/resources/{FONT_IMAGE}"


# ---------------------------------------------------------------------------
# GAME LOOP
# ---------------------------------------------------------------------------


def play_game(
    player: Entity,
    entities: List[Entity],
    game_map,
    message_log,
    game_state: GameStates,
    con,
    panel,
    constants: dict,
    fov_map: Optional[tcod.map.Map] = None,
) -> bool:
    """Main in-game loop."""
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = libtcodpy.Key()
    mouse = libtcodpy.Mouse()

    previous_game_state = game_state
    targeting_item: Optional[Entity] = None

    while not libtcodpy.console_is_window_closed():
        libtcodpy.sys_check_for_event(
            libtcodpy.EVENT_KEY_PRESS | libtcodpy.EVENT_MOUSE, key, mouse
        )

        # Simulate torch flickering by randomly adjusting the FOV radius each turn
        radius = constants["fov_radius"] + random.choice([0, 0, 1, -1])

        recompute_fov(
            fov_map,
            player.x,
            player.y,
            radius,
            constants["fov_light_walls"],
            constants["fov_algorithm"],
        )

        # Render everything
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
            radius,
        )

        fov_recompute = False
        libtcodpy.console_flush()
        clear_all(con, entities)

        # Handle input
        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get("move")
        wait = action.get("wait")
        pickup = action.get("pickup")
        show_inventory = action.get("show_inventory")
        drop_inventory = action.get("drop_inventory")
        inventory_index = action.get("inventory_index")
        take_stairs = action.get("take_stairs")
        level_up = action.get("level_up")
        show_character_screen = action.get("show_character_screen")
        exit_game = action.get("exit")
        full_screen = action.get("full_screen")

        left_click = mouse_action.get("left_click")
        right_click = mouse_action.get("right_click")

        player_turn_results = []

        inv = player.inventory
        f = player.fighter
        assert inv is not None
        assert f is not None

        # ------------------------------------------------------------------
        # PLAYER TURN
        # ------------------------------------------------------------------

        if move and game_state.is_player_turn:
            mv = move
            assert isinstance(mv, tuple)
            dx, dy = mv
            dest_x = player.x + dx
            dest_y = player.y + dy

            if not game_map.is_blocked(dest_x, dest_y):
                target = get_blocking_entities_at_location(entities, dest_x, dest_y)

                if target:
                    player_turn_results.extend(f.attack(target))
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        elif wait:
            game_state = GameStates.ENEMY_TURN

        elif pickup and game_state.is_player_turn:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    player_turn_results.extend(inv.add_item(entity))
                    break
            else:
                message_log.add_message(
                    Message("There is nothing here to pick up.", Colors.yellow)
                )

        # Inventory menus
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if (
            inventory_index is not None
            and previous_game_state != GameStates.PLAYER_DEAD
            and inventory_index < len(inv.items)
        ):
            item = inv.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(
                    inv.use(item, entities=entities, fov_map=fov_map)
                )
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(inv.drop_item(item))

        # Stairs
        if take_stairs and game_state.is_player_turn:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    game_map, entities = game_map.next_floor(player, message_log, constants)

                    # REBUILD FOV MAP FOR NEW FLOOR
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True

                    libtcodpy.console_clear(con)
                    break
            else:
                message_log.add_message(
                    Message("There are no stairs here.", Colors.yellow)
                )

        # Level up
        if level_up:
            if level_up == "hp":
                f.base_max_hp += 20
                f.hp += 20
            elif level_up == "str":
                f.base_power += 1
            elif level_up == "def":
                f.base_defense += 1

            game_state = previous_game_state

        # Character screen
        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        # Targeting mode
        if game_state == GameStates.TARGETING:
            if left_click:
                tx, ty = left_click

                ti = targeting_item
                assert ti is not None

                player_turn_results.extend(
                    inv.use(
                        ti,
                        entities=entities,
                        fov_map=fov_map,
                        target_x=tx,
                        target_y=ty,
                    )
                )
            elif right_click:
                player_turn_results.append({"targeting_cancelled": True})

        # Exit game
        if exit_game:
            if game_state.is_modal:
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({"targeting_cancelled": True})
            else:
                if game_state != GameStates.PLAYER_DEAD:
                    save_game(player, entities, game_map, message_log, game_state)
                return True

        # Toggle fullscreen
        if full_screen:
            libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())

        # ------------------------------------------------------------------
        # PROCESS PLAYER TURN RESULTS
        # ------------------------------------------------------------------

        for result in player_turn_results:
            message = result.get("message")
            dead_entity = result.get("dead")
            item_added = result.get("item_added")
            item_consumed = result.get("consumed")
            item_dropped = result.get("item_dropped")
            equip = result.get("equip")
            targeting = result.get("targeting")
            targeting_cancelled = result.get("targeting_cancelled")
            xp = result.get("xp")

            if message:
                message_log.add_message(message)

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

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

            if equip:
                eqp = player.equipment
                assert eqp is not None

                for eq_result in eqp.toggle_equip(equip):
                    equipped = eq_result.get("equipped")
                    dequipped = eq_result.get("dequipped")

                    if equipped:
                        message_log.add_message(
                            Message(
                                f"You equipped the {equipped.name}",
                                Colors.dark_green,
                            )
                        )
                    if dequipped:
                        message_log.add_message(
                            Message(
                                f"You dequipped the {dequipped.name}",
                                Colors.light_green,
                            )
                        )

                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                targeting_item = targeting
                assert targeting_item is not None
                assert targeting_item.item is not None
                message_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state
                message_log.add_message(Message("Targeting cancelled", Colors.yellow))

            
            lvl = player.level
            assert lvl is not None

            if xp:
                leveled = lvl.add_xp(xp)
                message_log.add_message(
                    Message(f"You gain {xp} experience points", Colors.green)
                )

                if leveled:
                    message_log.add_message(
                        Message(
                            f"Your battle skills grow stronger! You reached level {lvl.current_level}!",
                            Colors.yellow,
                        )
                    )
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

        # ------------------------------------------------------------------
        # ENEMY TURN
        # ------------------------------------------------------------------

        if game_state.is_enemy_turn:
            for entity in entities:
                if entity.fighter:
                    turn_results = entity.fighter.on_turn(entity)
                    for result in turn_results:
                        message = result.get("message")
                        # dead = result.get("dead")

                        if message:
                            message_log.add_message(message)

                if entity.ai:

                    for result in entity.ai.take_turn(
                        player, fov_map, game_map, entities
                    ):
                        message = result.get("message")
                        dead_entity = result.get("dead")

                        if message:
                            message_log.add_message(message)

                        if dead_entity == player:
                            backup_path = GAME_FILE + ".bak"
                            save_path = GAME_FILE + ".dat"

                            # Restore backup so Continue loads the previous floor
                            if os.path.exists(backup_path):
                                shutil.copy(backup_path, save_path)

                            message_log.add_message(Message("You died!", Colors.red))
                            game_state = GameStates.PLAYER_DEAD
                            break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN

    return False

# ---------------------------------------------------------------------------
# MAIN MENU / ENTRY POINT
# ---------------------------------------------------------------------------


def main() -> None:
    constants = get_constants()

    libtcodpy.console_set_custom_font(
        CUSTOM_FONT, libtcodpy.FONT_TYPE_GRAYSCALE | libtcodpy.FONT_LAYOUT_TCOD
    )

    libtcodpy.console_init_root(
        constants["screen_width"],
        constants["screen_height"],
        constants["window_title"],
        constants["full_screen"],
        constants["renderer"],
        "F",
        True,
    )

    con = libtcodpy.console_new(constants["screen_width"], constants["screen_height"])
    panel = libtcodpy.console_new(constants["screen_width"], constants["panel_height"])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = tcod.image.Image.from_file(MENU_BACKGROUND)

    key = libtcodpy.Key()
    mouse = libtcodpy.Mouse()

    while not libtcodpy.console_is_window_closed():
        libtcodpy.sys_check_for_event(
            libtcodpy.EVENT_KEY_PRESS | libtcodpy.EVENT_MOUSE, key, mouse
        )

        if show_main_menu:
            main_menu(
                con,
                main_menu_background_image,
                constants["screen_width"],
                constants["screen_height"],
            )

            if show_load_error_message:
                message_box(
                    con,
                    "No save game to load",
                    50,
                    constants["screen_width"],
                    constants["screen_height"],
                )

            libtcodpy.console_flush()

            action = handle_main_menu(key)

            new_game = action.get("new_game")
            load_saved_game = action.get("load_game")
            exit_game = action.get("exit")

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False

            elif new_game:
                (
                    player,
                    entities,
                    game_map,
                    message_log,
                    game_state,
                ) = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN
                show_main_menu = False

            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True

            elif exit_game:
                break

        else:
            assert player is not None
            assert game_state is not None
            
            libtcodpy.console_clear(con)
            play_game(
                player,
                entities,
                game_map,
                message_log,
                game_state,
                con,
                panel,
                constants,
            )
            show_main_menu = True


if __name__ == "__main__":
    main()
