from typing import NamedTuple


class Color(NamedTuple):
    r: int
    g: int
    b: int


class Colors:
    # General colors
    black = Color(0, 0, 0)
    grey = Color(127, 127, 127)
    dark_grey = Color(63, 63, 63)
    light_grey = Color(127, 127, 127)
    white = Color(255, 255, 255)
    pink = Color(255, 0, 255)
    dark_pink = Color(127, 0, 127)
    light_pink = Color(255, 127, 255)
    red = Color(255, 0, 0)
    dark_red = Color(127, 0, 0)
    light_red = Color(255, 63, 63)
    orange = Color(255, 127, 0)
    dark_orange = Color(191, 63, 0)
    light_orange = Color(255, 191, 127)
    yellow = Color(255, 255, 63)
    dark_yellow = Color(191, 191, 0)
    light_yellow = Color(255, 255, 127)
    green = Color(0, 255, 0)
    dark_green = Color(0, 127, 0)
    light_green = Color(127, 255, 127)
    desaturated_green = Color(63, 127, 63)
    blue = Color(0, 0, 255)
    dark_blue = Color(0, 0, 191)
    light_blue = Color(63, 63, 255)
    cyan = Color(0, 255, 255)
    dark_cyan = Color(0, 191, 191)
    light_cyan = Color(63, 255, 255)
    sky = Color(0, 191, 255)
    violet = Color(127, 0, 255)
    dark_violet = Color(63, 0, 191)
    light_violet = Color(191, 63, 255)

    # UI colors
    menu_title = Color(255, 255, 63)
    menu_text = Color(255, 255, 255)

    # Dungeon colors
    dark_wall = Color(0, 0, 100)
    dark_ground = Color(50, 50, 150)
    light_wall = Color(130, 110, 50)
    light_ground = Color(200, 180, 50)
    floor_dark = Color(50, 50, 150)
    floor_light = Color(200, 180, 50)
    wall_dark = Color(0, 0, 100)
    wall_light = Color(130, 110, 50)

    # Entities
    player = Color(255, 255, 255)
    orc = Color(63, 127, 63)
    troll = Color(0, 127, 0)
