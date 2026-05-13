from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Optional, List

from tcod import libtcodpy

from roguelike.colors import Color
from roguelike.components.equipment import Equipment
from roguelike.components.equippable import Equippable
from roguelike.components.fighter import Fighter
from roguelike.components.inventory import Inventory
from roguelike.components.item import Item
from roguelike.components.level import Level
from roguelike.components.stairs import Stairs
from roguelike.render_functions import RenderOrder


@dataclass
class Entity:
    """
    A generic object in the game world: player, monster, item, stairs, etc.
    """
    x: int
    y: int
    char: str
    color: Color
    name: str
    blocks: bool = False
    render_order: RenderOrder = RenderOrder.CORPSE

    fighter: Optional[Fighter] = None
    ai: Optional[Any] = None
    item: Optional[Item] = None
    inventory: Optional[Inventory] = None
    stairs: Optional[Stairs] = None
    level: Optional[Level] = None
    equipment: Optional[Equipment] = None
    equippable: Optional[Equippable] = None
    is_player: bool = False

    # ----------------------------------------------------------------------
    # Initialization
    # ----------------------------------------------------------------------
    def __post_init__(self):
        # Bind component ownership
        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            # Ensure equippable items also have an Item component
            if not self.item:
                self.item = Item()
                self.item.owner = self

        # Player always renders on top
        if getattr(self, "is_player", False) or self.name == "Player":
            self.render_order = RenderOrder.PLAYER

    @property
    def is_monster(self) -> bool:
        return not self.is_player and self.fighter is not None
    
    # ----------------------------------------------------------------------
    # Movement
    # ----------------------------------------------------------------------
    def move(self, dx: int, dy: int) -> None:
        """Move the entity by a delta."""
        self.x += dx
        self.y += dy

    def move_towards(self, target_x: int, target_y: int, game_map, entities: List[Entity]):
        """Move one step toward a target coordinate."""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance == 0:
            return

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (
            game_map.is_blocked(self.x + dx, self.y + dy)
            or get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)
        ):
            self.move(dx, dy)

    # ----------------------------------------------------------------------
    # A* Pathfinding (legacy TCOD API)
    # ----------------------------------------------------------------------
    def move_astar(self, target: Entity, entities: List[Entity], game_map):
        """
        Move toward the target using A* pathfinding.
        Uses deprecated libtcodpy API — will be replaced when TCOD is upgraded.
        """
        fov = libtcodpy.map_new(game_map.width, game_map.height)

        # Set walkable tiles
        for y in range(game_map.height):
            for x in range(game_map.width):
                libtcodpy.map_set_properties(
                    fov,
                    x,
                    y,
                    not game_map.tiles[x][y].block_sight,
                    not game_map.tiles[x][y].blocked,
                )

        # Mark blocking entities
        for entity in entities:
            if entity.blocks and entity is not self and entity is not target:
                libtcodpy.map_set_properties(fov, entity.x, entity.y, True, False)

        # Compute path
        path = libtcodpy.path_new_using_map(fov, 1.41)
        libtcodpy.path_compute(path, self.x, self.y, target.x, target.y)

        if not libtcodpy.path_is_empty(path) and libtcodpy.path_size(path) < 25:
            x, y = libtcodpy.path_walk(path, True)
            if x is not None and y is not None:
                self.x = x
                self.y = y
        else:
            self.move_towards(target.x, target.y, game_map, entities)

        libtcodpy.path_delete(path)

    # ----------------------------------------------------------------------
    # Distance helpers
    # ----------------------------------------------------------------------
    def distance(self, x: int, y: int) -> float:
        return math.hypot(x - self.x, y - self.y)

    def distance_to(self, other: Entity) -> float:
        return math.hypot(other.x - self.x, other.y - self.y)


# --------------------------------------------------------------------------
# Helper function
# --------------------------------------------------------------------------
def get_blocking_entities_at_location(entities: List[Entity], x: int, y: int) -> Optional[Entity]:
    """Return the blocking entity at a location, if any."""
    for entity in entities:
        if entity.blocks and entity.x == x and entity.y == y:
            return entity
    return None
