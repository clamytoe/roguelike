from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Stairs:
    """
    Represents a staircase leading to another dungeon floor.
    The `floor` attribute indicates which floor this staircase leads to.
    """
    floor: int
    owner: Optional[Any] = None  # Entity that owns this component

    def __repr__(self) -> str:
        return f"Stairs(floor={self.floor}, owner={self.owner})"

    def leads_to(self) -> int:
        """Return the floor number this staircase leads to."""
        return self.floor
