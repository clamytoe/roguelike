from enum import Enum, auto

import tcod

from roguelike.menus import inventory_menu

from .game_states import GameStates


class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def get_names_under_mouse(mouse, entities, fov_map):
    x, y = (mouse.cx, mouse.cy)

    names = [
        entity.name
        for entity in entities
        if entity.x == x
        and entity.y == y
        and tcod.map_is_in_fov(fov_map, entity.x, entity.y)
    ]
    names = ", ".join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)
    tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(
        panel,
        int(x + total_width / 2),
        y,
        tcod.BKGND_NONE,
        tcod.CENTER,
        f"{name}: {value}/{maximum}",
    )


def render_all(
    con,
    panel,
    entities,
    player,
    game_map,
    fov_map,
    fov_recompute,
    message_log,
    screen_width,
    screen_height,
    bar_width,
    panel_height,
    panel_y,
    mouse,
    colors,
    game_state,
):
    """
    Dra all entities in the list
    :param con: Console window to draw on
    :param panel: Console window for the stats information
    :param entities: List of entities to draw
    :param player: Player character class
    :param game_map: GameMap object
    :param fov_map: Field of View map
    :param fov_recompute: Boolean flag to determine if FOV should be recomputed
    :param message_log: MessageLog object with Messages
    :param screen_width: Width of the screen
    :param screen_height: Height of the screen
    :param bar_width: Width of the health bar
    :param panel_height: Height of the panel
    :param panel_y: Placement of the panel with respect to the main console window
    :param mouse: Mouse pointer object
    :param colors: GameMap color values
    :param game_state: GameState
    :return: None
    """
    # Draw all the tiles in the game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        tcod.console_set_char_background(
                            con, x, y, colors.get("light_wall"), tcod.BKGND_SET
                        )
                    else:
                        tcod.console_set_char_background(
                            con, x, y, colors.get("light_ground"), tcod.BKGND_SET
                        )

                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(
                            con, x, y, colors.get("dark_wall"), tcod.BKGND_SET
                        )
                    else:
                        tcod.console_set_char_background(
                            con, x, y, colors.get("dark_ground"), tcod.BKGND_SET
                        )

    # Draw all entities in the list
    entities_in_render_order = sorted(entities, key=lambda e: e.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        tcod.console_set_default_foreground(panel, message.color)
        tcod.console_print_ex(
            panel, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text
        )
        y += 1

    render_bar(
        panel,
        1,
        1,
        bar_width,
        "HP",
        player.fighter.hp,
        player.fighter.max_hp,
        tcod.light_red,
        tcod.darker_red,
    )

    tcod.console_set_default_foreground(panel, tcod.light_gray)
    tcod.console_print_ex(
        panel,
        1,
        0,
        tcod.BKGND_NONE,
        tcod.LEFT,
        get_names_under_mouse(mouse, entities, fov_map),
    )

    tcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = (
                "Press the key next to an item to use it, or ESC to cancel.\n"
            )
        else:
            inventory_title = (
                "Press the key next to an item to drop it, or ESC to cancel.\n"
            )

        inventory_menu(
            con, inventory_title, player.inventory, 50, screen_width, screen_height
        )


def clear_all(con, entities):
    """
    Loops over all entities passed and clears them from the screen
    :param con: Console window
    :param entities: List of entities to clear
    :return: None
    """
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map):
    """
    Draw an entity on the screen
    :param con: Console window
    :param entity: Entity object to draw
    :param fov_map: Field of View map
    :param game_map: GameMap object
    :return:
    """
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y) or (
        entity.stairs and game_map.tiles[entity.x][entity.y].explored
    ):
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


def clear_entity(con, entity):
    """
    erase the character that represents this object
    :param con: Console window
    :param entity: Entity object
    :return: None
    """
    tcod.console_put_char(con, entity.x, entity.y, " ", tcod.BKGND_NONE)
