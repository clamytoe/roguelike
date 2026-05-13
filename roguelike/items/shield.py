from roguelike.colors import Colors
from roguelike.components.equippable import Equippable
from roguelike.entity import Entity
from roguelike.equipment_slots import EquipmentSlots


class Shield(Entity):
    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            char="[",
            color=Colors.dark_orange,
            name="Shield",
            equippable=Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1),
        )
