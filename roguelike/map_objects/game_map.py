from __future__ import annotations

from dataclasses import dataclass, field
from random import randint
from typing import List, Optional, Dict, Tuple

from roguelike.colors import Colors
from roguelike.components.ai import BasicMonster
from roguelike.components.equipment import Equipment
from roguelike.components.equippable import Equippable
from roguelike.components.fighter import Fighter
from roguelike.components.item import Item
from roguelike.components.stairs import Stairs
from roguelike.entity import Entity
from roguelike.equipment_slots import EquipmentSlots
from roguelike.game_messages import Message
from roguelike.item_functions import (
    cast_confuse,
    cast_fireball,
    cast_lightning,
    heal,
)
from roguelike.random_utils import from_dungeon_level, random_choice_from_dict
from roguelike.render_functions import RenderOrder

from .rectangle import Rect
from .tile import Tile


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

    def __post_init__(self):
        self.tiles = self.initialize_tiles()

    # ----------------------------------------------------------------------
    # TILE INITIALIZATION
    # ----------------------------------------------------------------------
    def initialize_tiles(self) -> List[List[Tile]]:
        """Create a fully blocked map."""
        return [
            [Tile(blocked=True) for _ in range(self.height)]
            for _ in range(self.width)
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
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

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

            self.place_entities(new_room, entities)

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
        if randint(0, 1):
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

    # ----------------------------------------------------------------------
    # ENTITY PLACEMENT
    # ----------------------------------------------------------------------
    def place_entities(self, room: Rect, entities: List[Entity]) -> None:
        max_monsters = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)

        num_monsters = randint(0, max_monsters)
        num_items = randint(0, max_items)

        monster_chances = {
            "orc": 80,
            "troll": from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level),
        }

        item_chances = {
            "healing_potion": 35,
            "sword": from_dungeon_level([[5, 4]], self.dungeon_level),
            "shield": from_dungeon_level([[15, 8]], self.dungeon_level),
            "lightning_scroll": from_dungeon_level([[25, 4]], self.dungeon_level),
            "fireball_scroll": from_dungeon_level([[25, 6]], self.dungeon_level),
            "confusion_scroll": from_dungeon_level([[10, 2]], self.dungeon_level),
        }

        # Monsters
        for _ in range(num_monsters):
            x, y = self.random_room_position(room)
            if not self.is_occupied(x, y, entities):
                entities.append(self.create_monster(x, y, monster_chances))

        # Items
        for _ in range(num_items):
            x, y = self.random_room_position(room)
            if not self.is_occupied(x, y, entities):
                entities.append(self.create_item(x, y, item_chances))

    def random_room_position(self, room: Rect) -> Tuple[int, int]:
        return (
            randint(room.x1 + 1, room.x2 - 1),
            randint(room.y1 + 1, room.y2 - 1),
        )

    def is_occupied(self, x: int, y: int, entities: List[Entity]) -> bool:
        return any(e.x == x and e.y == y for e in entities)

    # ----------------------------------------------------------------------
    # MONSTER / ITEM FACTORIES
    # ----------------------------------------------------------------------
    def create_monster(self, x: int, y: int, chances: Dict[str, int]) -> Entity:
        choice = random_choice_from_dict(chances)

        if choice == "orc":
            fighter = Fighter(hp=20, defense=0, power=4, xp=35)
            ai = BasicMonster()
            return Entity(
                x, y, "o", Colors.desaturated_green, "Orc",
                blocks=True, render_order=RenderOrder.ACTOR,
                fighter=fighter, ai=ai
            )

        # Troll
        fighter = Fighter(hp=30, defense=2, power=8, xp=100)
        ai = BasicMonster()
        return Entity(
            x, y, "T", Colors.dark_green, "Troll",
            blocks=True, render_order=RenderOrder.ACTOR,
            fighter=fighter, ai=ai
        )

    def create_item(self, x: int, y: int, chances: Dict[str, int]) -> Entity:
        choice = random_choice_from_dict(chances)

        if choice == "healing_potion":
            item = Item(use_function=heal, amount=40)
            return Entity(
                x, y, "!", Colors.violet, "Healing Potion",
                render_order=RenderOrder.ITEM, item=item
            )

        if choice == "sword":
            eq = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
            return Entity(x, y, "/", Colors.sky, "Sword", equippable=eq)

        if choice == "shield":
            eq = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
            return Entity(x, y, "[", Colors.dark_orange, "Shield", equippable=eq)

        if choice == "fireball_scroll":
            item = Item(
                use_function=cast_fireball,
                targeting=True,
                targeting_message=Message(
                    "Left-click a target tile for the fireball, or right-click to cancel",
                    Colors.light_cyan,
                ),
                damage=25,
                radius=3,
            )
            return Entity(
                x, y, "#", Colors.red, "Fireball Scroll",
                render_order=RenderOrder.ITEM, item=item
            )

        if choice == "confusion_scroll":
            item = Item(
                use_function=cast_confuse,
                targeting=True,
                targeting_message=Message(
                    "Left-click an enemy to confuse it, or right-click to cancel.",
                    Colors.light_cyan,
                ),
            )
            return Entity(
                x, y, "#", Colors.light_pink, "Confusion Scroll",
                render_order=RenderOrder.ITEM, item=item
            )

        # Lightning scroll
        item = Item(use_function=cast_lightning, damage=40, maximum_range=5)
        return Entity(
            x, y, "#", Colors.yellow, "Lightning Scroll",
            render_order=RenderOrder.ITEM, item=item
        )

    # ----------------------------------------------------------------------
    # BLOCKING / NEXT FLOOR
    # ----------------------------------------------------------------------
    def is_blocked(self, x: int, y: int) -> bool:
        return self.tiles[x][y].blocked

    def next_floor(self, player: Entity, message_log, constants) -> Tuple[GameMap, List[Entity]]:
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
