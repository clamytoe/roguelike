from dataclasses import dataclass
from typing import Union


@dataclass
class Tile:
    """
    A tile on a map.

    It may or may not be blocked, and may or may not block sight.
    """

    blocked: bool
    block_sight: Union[bool, None] = None

    def __post_init__(self):
        self.block_sight = (
            self.blocked if self.block_sight is None else self.block_sight
        )
