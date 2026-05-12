from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Rect:
    """Axis-aligned rectangle used for dungeon room generation."""
    x1: int
    y1: int
    w: int
    h: int

    # Computed fields (populated in __post_init__)
    x2: int = 0
    y2: int = 0

    def __post_init__(self) -> None:
        # x2/y2 are exclusive bounds (right/bottom edges)
        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h

    def center(self) -> tuple[int, int]:
        """Return the integer center point of the rectangle."""
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    def intersect(self, other: Rect) -> bool:
        """Return True if this rectangle intersects another."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
