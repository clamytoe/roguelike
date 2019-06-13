#!/usr/bin/env python3
"""
app.py

Roguelike Game
"""
from os import path

import tcod
import tcod.event

from .entity import Entity
from .input_handlers import handle_keys
from .map_objects.game_map import GameMap
from .render_functions import clear_all, clear_entity, draw_entity, render_all

TITLE = "roguelike tutorial"
FONT_IMAGE = "arial10x10.png"
HERE = path.abspath(path.dirname(__file__))
CUSTOM_FONT = f"{HERE}/img/{FONT_IMAGE}"
FULL_SCREEN = False
PLAYER_BG = tcod.BKGND_NONE
MAP_WIDTH = 80
MAP_HEIGHT = 45
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
COLORS = {
    "dark_wall": tcod.Color(0, 0, 100),
    "dark_ground": tcod.Color(50, 50, 150),
}


def main():
    npc = Entity(int(SCREEN_WIDTH / 2 - 5), int(SCREEN_HEIGHT / 2), "*", tcod.white)
    player = Entity(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), "@", tcod.white)
    entities = [npc, player]

    tcod.console_set_custom_font(
        CUSTOM_FONT, tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_TCOD
    )

    with tcod.console_init_root(
        SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FULL_SCREEN, tcod.RENDERER_SDL2, "F", True
    ) as con:
        key = tcod.Key()
        mouse = tcod.Mouse()
        game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)

        while not tcod.console_is_window_closed():
            tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
            render_all(con, entities, game_map, SCREEN_WIDTH, SCREEN_HEIGHT, COLORS)

            tcod.console_flush()

            clear_all(con, entities)

            action = handle_keys(key)

            move = action.get("move")
            exit = action.get("exit")
            fullscreen = action.get("fullscreen")

            if move:
                dx, dy = move
                player.move(dx, dy)

            if exit:
                return True

            if fullscreen:
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
