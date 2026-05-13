from __future__ import annotations

import random
from dataclasses import dataclass, field

# from random import randint
from typing import Dict, List, Tuple

from roguelike.colors import Colors
from roguelike.components.ai import BasicMonster
from roguelike.components.equippable import Equippable
from roguelike.components.fighter import Fighter
from roguelike.components.item import Item
from roguelike.components.stairs import Stairs
from roguelike.entity import Entity
from roguelike.equipment_slots import EquipmentSlots
from roguelike.game_messages import Message
from roguelike.items import ITEM_WEIGHTS
from roguelike.monsters.monster_tables import get_monster_for_depth
from roguelike.random_utils import from_dungeon_level, random_choice_from_dict
from roguelike.render_functions import RenderOrder

from .rectangle import Rect
from .tile import Tile

SAFE_RADIUS = 6  # prevents monsters from spawning in starting room

# ---------------------------------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------------------------------
def weighted_choice(rng, weighted_list):
    """Return a class chosen from a weighted list of (cls, weight)."""
    total = sum(weight for _, weight in weighted_list)
    roll = rng.randint(0, total - 1)

    for monster_cls, weight in weighted_list:
        if roll < weight:
            return monster_cls
        roll -= weight

    return weighted_list[-1][0]


# ---------------------------------------------------------------------------
# GAME MAP
# ---------------------------------------------------------------------------


@dataclass
class GameMap:
    """
    Represents the dungeon map, including tiles, rooms, entities, and generation.
    """

    width: int
    height: int
    tiles: List[List[Tile]] = field(default_factory=list)
    dungeon_level: int = 1
    seed: int = field(default_factory=lambda: random.randint(0, 2**32 - 1))
    rng: random.Random = field(init=False)

    def __post_init__(self):
        self.tiles = self.initialize_tiles()
        self.rng = random.Random(self.seed)

    # ----------------------------------------------------------------------
    # TILE INITIALIZATION
    # ----------------------------------------------------------------------
    def initialize_tiles(self) -> List[List[Tile]]:
        """Create a fully blocked map."""
        return [
            [Tile(blocked=True) for _ in range(self.height)] for _ in range(self.width)
        ]

    # ----------------------------------------------------------------------
    # MAP GENERATION
    # ----------------------------------------------------------------------
    def make_map(
        self,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        player: Entity,
        entities: List[Entity],
    ) -> None:
        """
        Generate a new dungeon layout using the classic room-and-corridor algorithm.
        """
        rooms: List[Rect] = []
        last_center: Tuple[int, int] = (0, 0)

        for _ in range(max_rooms):
            w = self.rng.randint(room_min_size, room_max_size)
            h = self.rng.randint(room_min_size, room_max_size)
            x = self.rng.randint(0, map_width - w - 1)
            y = self.rng.randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            if any(new_room.intersect(other) for other in rooms):
                continue

            # Carve room
            self.create_room(new_room)
            new_x, new_y = new_room.center()

            if not rooms:
                player.x, player.y = new_x, new_y
            else:
                prev_x, prev_y = rooms[-1].center()
                self.connect_rooms(prev_x, prev_y, new_x, new_y)

            self.place_entities(new_room, entities, player)

            rooms.append(new_room)
            last_center = (new_x, new_y)

        # Place stairs in last room
        stairs_component = Stairs(self.dungeon_level + 1)
        stairs = Entity(
            last_center[0],
            last_center[1],
            ">",
            Colors.white,
            "Stairs",
            render_order=RenderOrder.STAIRS,
            stairs=stairs_component,
        )
        entities.append(stairs)

    # ----------------------------------------------------------------------
    # ROOM / TUNNEL CREATION
    # ----------------------------------------------------------------------
    def carve(self, x: int, y: int) -> None:
        """Mark a tile as walkable and transparent."""
        self.tiles[x][y].blocked = False
        self.tiles[x][y].block_sight = False

    def create_room(self, room: Rect) -> None:
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.carve(x, y)

    def connect_rooms(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Randomly choose tunnel order."""
        if self.rng.randint(0, 1):
            self.create_h_tunnel(x1, x2, y1)
            self.create_v_tunnel(y1, y2, x2)
        else:
            self.create_v_tunnel(y1, y2, x1)
            self.create_h_tunnel(x1, x2, y2)

    def create_h_tunnel(self, x1: int, x2: int, y: int) -> None:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.carve(x, y)

    def create_v_tunnel(self, y1: int, y2: int, x: int) -> None:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.carve(x, y)

    def distance(self, x1, y1, x2, y2):
        return max(abs(x1 - x2), abs(y1 - y2))

    # ----------------------------------------------------------------------
    # ENTITY PLACEMENT
    # ----------------------------------------------------------------------
    def place_entities(self, room: Rect, entities: List[Entity], player: Entity) -> None:
        max_monsters = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)

        num_monsters = self.rng.randint(0, max_monsters)
        num_items = self.rng.randint(0, max_items)

        # Monsters
        for _ in range(num_monsters):
            x, y = self.random_room_position(room)

            # Skip if tile is occupied
            if self.is_occupied(x, y, entities):
                continue

            # Skip if too close to the player
            if self.distance(x, y, player.x, player.y) < SAFE_RADIUS:
                continue

            monster_cls = get_monster_for_depth(self.rng, self.dungeon_level)
            monster = monster_cls(x, y)
            entities.append(monster)

        # Items
        for _ in range(num_items):
            x, y = self.random_room_position(room)
            if not self.is_occupied(x, y, entities):
                item_cls = weighted_choice(self.rng, ITEM_WEIGHTS)
                entities.append(item_cls(x, y))

    def random_room_position(self, room: Rect) -> Tuple[int, int]:
        return (
            self.rng.randint(room.x1 + 1, room.x2 - 1),
            self.rng.randint(room.y1 + 1, room.y2 - 1),
        )

    def is_occupied(self, x: int, y: int, entities: List[Entity]) -> bool:
        return any(e.x == x and e.y == y for e in entities)

    # ----------------------------------------------------------------------
    # BLOCKING / NEXT FLOOR
    # ----------------------------------------------------------------------
    def is_blocked(self, x: int, y: int) -> bool:
        return self.tiles[x][y].blocked

    def next_floor(
        self, player: Entity, message_log, constants
    ) -> Tuple[GameMap, List[Entity]]:
        """
        Advance to the next dungeon floor.
        Returns the new map and the new entity list.
        """
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(
            constants["max_rooms"],
            constants["room_min_size"],
            constants["room_max_size"],
            constants["map_width"],
            constants["map_height"],
            player,
            entities,
        )

        # Heal player to full
        assert player.fighter is not None
        player.fighter.hp = player.fighter.max_hp

        message_log.add_message(
            Message(
                "You take a moment to rest, and recover your strength.",
                Colors.light_violet,
            )
        )

        return self, entities
