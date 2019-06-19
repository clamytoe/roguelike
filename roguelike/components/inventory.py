from dataclasses import dataclass, field
from typing import List

import tcod

from roguelike.game_messages import Message

from .item import Item


@dataclass
class Inventory:
    capacity: int
    items: List[Item] = field(default_factory=list)

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append(
                {
                    "item_added": None,
                    "message": Message(
                        "You cannot carry any more, your inventory is full", tcod.yellow
                    ),
                }
            )
        else:
            results.append(
                {
                    "item_added": item,
                    "message": Message(f"You pick up the {item.name}", tcod.blue),
                }
            )

            self.items.append(item)

        return results
