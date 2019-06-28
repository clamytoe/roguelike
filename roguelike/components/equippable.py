from dataclasses import dataclass

from roguelike.equipment_slots import EquipmentSlots


@dataclass
class Equippable:
    slot: EquipmentSlots
    power_bonus: int = 0
    defense_bonus: int = 0
    max_hp_bonus: int = 0
