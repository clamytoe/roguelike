from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict, Any, TYPE_CHECKING

from roguelike.equipment_slots import EquipmentSlots

if TYPE_CHECKING:
    from roguelike.entity import Entity


@dataclass
class Equipment:
    """
    Handles equipping and unequipping items and provides total stat bonuses.
    """
    main_hand: Optional[Entity] = None
    off_hand: Optional[Entity] = None
    owner: Optional[Entity] = None

    # ----------------------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------------------
    def _equipped_items(self) -> List[Entity]:
        """Return a list of all currently equipped item entities."""
        items = []
        if self.main_hand:
            items.append(self.main_hand)
        if self.off_hand:
            items.append(self.off_hand)
        return items

    # ----------------------------------------------------------------------
    # Bonus properties
    # ----------------------------------------------------------------------
    @property
    def max_hp_bonus(self) -> int:
        return sum(
            item.equippable.max_hp_bonus
            for item in self._equipped_items()
            if item.equippable
        )

    @property
    def defense_bonus(self) -> int:
        return sum(
            item.equippable.defense_bonus
            for item in self._equipped_items()
            if item.equippable
        )

    @property
    def power_bonus(self) -> int:
        return sum(
            item.equippable.power_bonus
            for item in self._equipped_items()
            if item.equippable
        )

    # ----------------------------------------------------------------------
    # Equip / Unequip
    # ----------------------------------------------------------------------
    def toggle_equip(self, item_entity: Entity) -> List[Dict[str, Any]]:
        """
        Equip or unequip an item. Returns a list of results for the message log.
        """
        eqp = item_entity.equippable
        assert eqp is not None

        results: List[Dict[str, Any]] = []
        slot = eqp.slot

        # MAIN HAND
        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand is item_entity:
                self.main_hand = None
                results.append({"dequipped": item_entity})
                return results

            if self.main_hand:
                results.append({"dequipped": self.main_hand})

            self.main_hand = item_entity
            results.append({"equipped": item_entity})
            return results

        # OFF HAND
        if slot == EquipmentSlots.OFF_HAND:
            if self.off_hand is item_entity:
                self.off_hand = None
                results.append({"dequipped": item_entity})
                return results

            if self.off_hand:
                results.append({"dequipped": self.off_hand})

            self.off_hand = item_entity
            results.append({"equipped": item_entity})
            return results

        return results
