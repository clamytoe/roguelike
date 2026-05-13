from roguelike.colors import Colors
from roguelike.components.equippable import Equippable
from roguelike.entity import Entity
from roguelike.equipment_slots import EquipmentSlots


class Sword(Entity):
    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            char="/",
            color=Colors.sky,
            name="Sword",
            equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3),
        )
