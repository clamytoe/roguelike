from __future__ import annotations

from tcod import libtcodpy, map


def initialize_fov(game_map):
    """Create and initialize a TCOD FOV map from the game map."""
    fov_map = map.Map(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            tile = game_map.tiles[x][y]
            libtcodpy.map_set_properties(
                fov_map,
                x,
                y,
                not tile.block_sight,
                not tile.blocked,
            )

    return fov_map


def recompute_fov(
    fov_map, x, y, radius, light_walls=True, algorithm=libtcodpy.FOV_SHADOW
):
    """Recompute the field of view from a given position."""
    libtcodpy.map_compute_fov(
        fov_map,
        x,
        y,
        radius,
        light_walls,
        algorithm,
    )
