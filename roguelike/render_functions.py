import tcod


def render_all(
    con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors
):
    """
    Dra all entities in the list
    :param con: Console window to draw on
    :param entities: List of entities to draw
    :param game_map: GameMap object
    :param fov_map: Field of View map
    :param fov_recompute: Boolean flag to determine if FOV should be recomputed
    :param screen_width: Width of the screen
    :param screen_height: Height of the screen
    :param colors: GameMap color values
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
    for entity in entities:
        draw_entity(con, entity, fov_map)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, con, 0, 0)


def clear_all(con, entities):
    """
    Loops over all entities passed and clears them from the screen
    :param con: Console window
    :param entities: List of entities to clear
    :return: None
    """
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    """
    Draw an entity on the screen
    :param con: Console window
    :param entity: Entity object to draw
    :param fov_map: Field of View map
    :return:
    """
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
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
