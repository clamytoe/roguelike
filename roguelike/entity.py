from dataclasses import dataclass

from tcod.color import Color


@dataclass
class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    x: int
    y: int
    char: str
    color: Color
    name: str
    blocks: bool = False

    def move(self, dx: int, dy: int) -> None:
        """
        Move the entity by a given amount
        :param dx: Steps to move in the x-axis
        :param dy: Steps to move in the y-axis
        :return: None
        """
        self.x += dx
        self.y += dy


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
