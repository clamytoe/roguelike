from __future__ import annotations

import math
from enum import Enum, auto
from typing import cast, Tuple

from tcod import libtcodpy
from tcod.console import Console

from roguelike.colors import Colors
from roguelike.menus import character_screen, inventory_menu, level_up_menu

from .game_states import GameStates


class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
    PLAYER = auto()


def get_names_under_mouse(mouse, entities, fov_map) -> str:
    """Return a comma-separated list of entity names under the mouse cursor."""
    x, y = mouse.cx, mouse.cy

    names = [
        entity.name
        for entity in entities
        if entity.x == x
        and entity.y == y
        and libtcodpy.map_is_in_fov(fov_map, entity.x, entity.y)
    ]

    return ", ".join(names).title()


def lerp(a, b, t):
    """Linear interpolation between two RGB colors."""
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )


def render_bar(
    panel,
    x: int,
    y: int,
    total_width: int,
    name: str,
    value: int,
    maximum: int,
    bar_color: Tuple[int, int, int],
    back_color: Tuple[int, int, int],
) -> None:
    """Render a horizontal bar (HP, XP, etc.)."""
    bar_width = int(float(value) / maximum * total_width)

    libtcodpy.console_set_default_background(panel, back_color)
    libtcodpy.console_rect(panel, x, y, total_width, 1, False, libtcodpy.BKGND_SCREEN)

    libtcodpy.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcodpy.console_rect(panel, x, y, bar_width, 1, False, libtcodpy.BKGND_SCREEN)

    libtcodpy.console_set_default_foreground(panel, Colors.white)
    libtcodpy.console_print_ex(
        panel,
        x + total_width // 2,
        y,
        libtcodpy.BKGND_NONE,
        libtcodpy.CENTER,
        f"{name}: {value}/{maximum}",
    )


def render_all(
    con,
    panel,
    entities,
    player,
    game_map,
    fov_map,
    fov_recompute: bool,
    message_log,
    screen_width: int,
    screen_height: int,
    bar_width: int,
    panel_height: int,
    panel_y: int,
    mouse,
    colors,
    game_state: GameStates,
    radius: int,
) -> None:
    """Draw the entire game state: map, entities, UI, messages, menus."""
    # Draw map tiles
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcodpy.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    distance = math.hypot(x - player.x, y - player.y)
                    fade = max(0.0, 1.0 - distance / radius)

                    base = colors.light_wall if wall else colors.light_ground
                    dark = colors.dark_wall if wall else colors.dark_ground

                    bg = lerp(dark, base, fade)
                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    bg = colors.dark_wall if wall else colors.dark_ground

                else:
                    continue

                libtcodpy.console_set_char_background(con, x, y, bg, libtcodpy.BKGND_SET)

    # Draw entities
    entities_sorted = sorted(entities, key=lambda e: e.render_order.value)
    for entity in entities_sorted:
        draw_entity(con, entity, fov_map, game_map)

    # Blit main console
    libtcodpy.console_blit(con, 0, 0, screen_width, screen_height, cast(Console, 0), 0, 0)

    # Draw UI panel
    libtcodpy.console_set_default_background(panel, Colors.black)
    libtcodpy.console_clear(panel)

    # Messages
    y = 1
    for message in message_log.messages:
        libtcodpy.console_set_default_foreground(panel, message.color)
        libtcodpy.console_print_ex(
            panel, message_log.x, y, libtcodpy.BKGND_NONE, libtcodpy.LEFT, message.text
        )
        y += 1

    # HP bar
    render_bar(
        panel,
        1,
        1,
        bar_width,
        "HP",
        player.fighter.hp,
        player.fighter.max_hp,
        Colors.light_red,
        Colors.dark_red,
    )

    # Dungeon level
    libtcodpy.console_set_default_foreground(panel, Colors.light_grey)
    libtcodpy.console_print_ex(
        panel,
        1,
        3,
        libtcodpy.BKGND_NONE,
        libtcodpy.LEFT,
        f"Dungeon level: {game_map.dungeon_level}",
    )

    # Mouse hover names
    libtcodpy.console_print_ex(
        panel,
        1,
        0,
        libtcodpy.BKGND_NONE,
        libtcodpy.LEFT,
        get_names_under_mouse(mouse, entities, fov_map),
    )

    # Blit panel
    libtcodpy.console_blit(
        panel,
        0,
        0,
        screen_width,
        panel_height,
        cast(Console, 0),
        0,
        panel_y,   # ← correct destination Y
        1.0,
        1.0,
    )


    # Menus
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        title = (
            "Press the key next to an item to use it, or ESC to cancel.\n"
            if game_state == GameStates.SHOW_INVENTORY
            else "Press the key next to an item to drop it, or ESC to cancel.\n"
        )
        inventory_menu(con, title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(
            con,
            "Level up! Choose a stat to raise:",
            player,
            40,
            screen_width,
            screen_height,
        )

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)


def clear_all(con, entities) -> None:
    """Clear all entities from the console."""
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map) -> None:
    """Draw a single entity if visible or if stairs on explored tile."""
    if libtcodpy.map_is_in_fov(fov_map, entity.x, entity.y) or (
        entity.stairs and game_map.tiles[entity.x][entity.y].explored
    ):
        libtcodpy.console_set_default_foreground(con, entity.color)
        libtcodpy.console_put_char(
            con, entity.x, entity.y, entity.char, libtcodpy.BKGND_NONE
        )


def clear_entity(con, entity) -> None:
    """Erase the character representing this entity."""
    libtcodpy.console_put_char(con, entity.x, entity.y, " ", libtcodpy.BKGND_NONE)
