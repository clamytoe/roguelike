from __future__ import annotations

from typing import cast, List

from tcod import libtcodpy
from tcod.console import Console
from roguelike.colors import Colors


# ---------------------------------------------------------------------------
# GENERIC MENU
# ---------------------------------------------------------------------------

def menu(
    con,
    header: str,
    options: List[str],
    width: int,
    screen_width: int,
    screen_height: int,
) -> None:

    if len(options) > 26:
        raise ValueError("Cannot have a menu with more than 26 options.")

    # Calculate header height (auto-wrapped)
    header_height = libtcodpy.console_get_height_rect(
        con, 0, 0, width, screen_height, header
    )
    height = header_height + len(options)

    # Create window
    window = libtcodpy.console_new(width, height)
    libtcodpy.console_set_default_foreground(window, Colors.white)

    # Print header
    libtcodpy.console_print_rect_ex(
        window,
        0,
        0,
        width,
        height,
        libtcodpy.BKGND_NONE,
        libtcodpy.LEFT,
        header,
    )

    # Print options
    y = header_height
    letter = ord("a")

    for option in options:
        if option == "Inventory is empty.":
            text = f"( ) {option}"
        else:
            text = f"({chr(letter)}) {option}"

        libtcodpy.console_print_ex(
            window,
            0,
            y,
            libtcodpy.BKGND_NONE,
            libtcodpy.LEFT,
            text,
        )
        y += 1
        letter += 1

    # Center the menu
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    libtcodpy.console_blit(window, 0, 0, width, height, cast(Console, 0), x, y, 1.0, 0.7)


# ---------------------------------------------------------------------------
# INVENTORY MENU
# ---------------------------------------------------------------------------

def inventory_menu(
    con,
    header: str,
    player,
    inventory_width: int,
    screen_width: int,
    screen_height: int,
) -> None:

    if not player.inventory.items:
        options = ["Inventory is empty."]
    else:
        options = []
        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append(f"{item.name} (in main hand)")
            elif player.equipment.off_hand == item:
                options.append(f"{item.name} (in off hand)")
            else:
                options.append(item.name)

    menu(con, header, options, inventory_width, screen_width, screen_height)


# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------

def main_menu(con, background_image, screen_width: int, screen_height: int) -> None:
    libtcodpy.image_blit_2x(background_image, cast(Console, 0), 0, 0, 0)

    libtcodpy.console_set_default_foreground(cast(Console, 0), Colors.yellow)
    libtcodpy.console_print_ex(
        cast(Console, 0),
        screen_width // 2,
        screen_height - 2,
        libtcodpy.BKGND_NONE,
        libtcodpy.CENTER,
        "By clamytoe",
    )

    menu(
        con,
        "",
        ["Play a new game", "Continue last game", "Quit"],
        24,
        screen_width,
        screen_height,
    )


# ---------------------------------------------------------------------------
# LEVEL UP MENU
# ---------------------------------------------------------------------------

def level_up_menu(
    con,
    header: str,
    player,
    menu_width: int,
    screen_width: int,
    screen_height: int,
) -> None:

    options = [
        f"Constitution (+20 HP, from {player.fighter.max_hp})",
        f"Strength (+1 attack, from {player.fighter.power_level})",
        f"Agility (+1 defense, from {player.fighter.defense_level})",
    ]

    menu(con, header, options, menu_width, screen_width, screen_height)


# ---------------------------------------------------------------------------
# CHARACTER SCREEN
# ---------------------------------------------------------------------------

def character_screen(
    player,
    width: int,
    height: int,
    screen_width: int,
    screen_height: int,
) -> None:

    window = libtcodpy.console_new(width, height)
    libtcodpy.console_set_default_foreground(window, Colors.white)

    lines = [
        "Character Information",
        f"Level: {player.level.current_level}",
        f"Experience: {player.level.current_xp}",
        f"Experience to Level: {player.level.experience_to_next_level}",
        "",
        f"Maximum HP: {player.fighter.max_hp}",
        f"Attack: {player.fighter.power_level}",
        f"Defense: {player.fighter.defense_level}",
    ]

    for i, line in enumerate(lines):
        libtcodpy.console_print_rect_ex(
            window,
            0,
            i + 1,
            width,
            height,
            libtcodpy.BKGND_NONE,
            libtcodpy.LEFT,
            line,
        )

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    libtcodpy.console_blit(window, 0, 0, width, height, cast(Console, 0), x, y, 1.0, 0.7)


# ---------------------------------------------------------------------------
# MESSAGE BOX
# ---------------------------------------------------------------------------

def message_box(con, header: str, width: int, screen_width: int, screen_height: int):
    menu(con, header, [], width, screen_width, screen_height)
