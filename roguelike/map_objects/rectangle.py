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
