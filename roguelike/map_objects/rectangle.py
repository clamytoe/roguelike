from dataclasses import dataclass


@dataclass
class Rect:
    x1: int
    y1: int
    w: int
    h: int

    def __post_init__(self):
        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
