from dataclasses import dataclass


@dataclass
class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    x: int
    y: int
    char: str
    color: int

    def move(self, dx: int, dy: int) -> None:
        """
        Move the entity by a given amount
        :param dx: Steps to move in the x-axis
        :param dy: Steps to move in the y-axis
        :return: None
        """
        self.x += dx
        self.y += dy
