from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict, TYPE_CHECKING

from roguelike.colors import Colors
from roguelike.game_messages import Message

if TYPE_CHECKING:
    from roguelike.entity import Entity

@dataclass
class Inventory:
    capacity: int
    items: List["Entity"] = field(default_factory=list)
    owner: Optional[Any] = None

    # ----------------------------------------------------------------------
    # ADD ITEM
    # ----------------------------------------------------------------------
    def add_item(self, item: "Entity") -> List[Dict[str, Any]]:
        if len(self.items) >= self.capacity:
            return [{
                "item_added": None,
                "message": Message(
                    "You cannot carry any more, your inventory is full.",
                    Colors.yellow,
                ),
            }]

        self.items.append(item)
        return [{
            "item_added": item,
            "message": Message(f"You pick up the {item.name}.", Colors.blue),
        }]

    # ----------------------------------------------------------------------
    # USE ITEM
    # ----------------------------------------------------------------------
    def use(self, item_entity: "Entity", **kwargs) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        item_component = item_entity.item
        assert item_component is not None

        # No use function → maybe equippable
        if item_component.use_function is None:
            if item_entity.equippable:
                return [{"equip": item_entity}]
            return [{
                "message": Message(
                    f"The {item_entity.name} cannot be used.",
                    Colors.yellow,
                )
            }]

        # Targeting required but no target provided
        if item_component.targeting and not (
            kwargs.get("target_x") or kwargs.get("target_y")
        ):
            return [{"targeting": item_entity}]

        # Merge parameters cleanly
        params = {
            "amount": item_component.amount,
            "damage": item_component.damage,
            "radius": item_component.radius,
            "maximum_range": item_component.maximum_range,
            **item_component.function_kwargs,
            **kwargs,
        }

        # Execute item function
        item_use_results = item_component.use_function(self.owner, **params)

        # Remove item if consumed
        for result in item_use_results:
            if result.get("consumed"):
                self.remove_item(item_entity)

        return item_use_results

    # ----------------------------------------------------------------------
    # REMOVE ITEM
    # ----------------------------------------------------------------------
    def remove_item(self, item: "Entity") -> None:
        if item in self.items:
            self.items.remove(item)

    # ----------------------------------------------------------------------
    # DROP ITEM
    # ----------------------------------------------------------------------
    def drop_item(self, item: "Entity") -> List[Dict[str, Any]]:
        assert self.owner is not None
        results: List[Dict[str, Any]] = []

        # Unequip if equipped
        if (
            self.owner.equipment.main_hand == item
            or self.owner.equipment.off_hand == item
        ):
            self.owner.equipment.toggle_equip(item)

        # Drop at player's feet
        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)

        results.append({
            "item_dropped": item,
            "message": Message(f"You dropped the {item.name}.", Colors.yellow),
        })

        return results
