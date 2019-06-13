from dataclasses import dataclass, field
from typing import List

from .tile import Tile


@dataclass
class GameMap:
    width: int
    height: int
    tiles: List[List[Tile]] = field(default_factory=list)

    def __post_init__(self):
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True

        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
