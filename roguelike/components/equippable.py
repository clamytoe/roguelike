from dataclasses import dataclass
from typing import Any, Optional

from roguelike.equipment_slots import EquipmentSlots


@dataclass
class Equippable:
    slot: EquipmentSlots
    power_bonus: int = 0
    defense_bonus: int = 0
    max_hp_bonus: int = 0
    two_handed: bool = False
    value: int = 0
    rarity: int = 0

    owner: Optional[Any] = None
