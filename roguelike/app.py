#!/usr/bin/env python3
"""
app.py

Roguelike Game
"""
from os import path

import tcod as libtcod

TITLE = "roguelike tutorial"
FONT_IMAGE = "arial10x10.png"
HERE = path.abspath(path.dirname(__file__))
CUSTOM_FONT = f"{HERE}/img/{FONT_IMAGE}"
FULL_SCREEN = False
MAIN_SCREEN = 0
PLAYER_CHAR = "@"
PLAYER_COLOR = libtcod.white
PLAYER_BG = libtcod.BKGND_NONE
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50


def main():
    libtcod.console_set_custom_font(
        CUSTOM_FONT, libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD
    )
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FULL_SCREEN)

    while not libtcod.console_is_window_closed():
        libtcod.console_set_default_foreground(MAIN_SCREEN, PLAYER_COLOR)
        libtcod.console_put_char(MAIN_SCREEN, 1, 1, PLAYER_CHAR, PLAYER_BG)
        libtcod.console_flush()

        key = libtcod.console_check_for_keypress()

        if key.vk == libtcod.KEY_ESCAPE:
            return True


if __name__ == "__main__":
    main()
