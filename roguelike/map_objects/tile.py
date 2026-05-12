from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Tile:
    """
    A tile on the map.

    - `blocked`: whether movement is blocked.
    - `block_sight`: whether the tile blocks line of sight.
      If None, it defaults to the same value as `blocked`.
    - `explored`: whether the player has seen this tile before.
    """

    blocked: bool
    block_sight: Optional[bool] = None
    explored: bool = False

    def __post_init__(self) -> None:
        # If block_sight is not explicitly set, match it to `blocked`.
        if self.block_sight is None:
            self.block_sight = self.blocked
