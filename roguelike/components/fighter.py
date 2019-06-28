from dataclasses import dataclass
from typing import Any, List, Union

import tcod

from roguelike.components.equipment import Equipment
from roguelike.game_messages import Message


@dataclass
class Fighter:
    hp: int
    defense: int
    power: int
    name: str = ""
    xp: int = 0
    base_max_hp: int = 0
    base_defense: int = 0
    base_power: int = 0
    owner: Union[Any, None] = None
    equipment: Union[List[Equipment], None] = None

    def __post_init__(self):
        self.owner = self
        self.base_max_hp = self.hp
        self.base_defense = self.defense_level
        self.base_power = self.power

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power_level(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense_level(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount):
        results = []
        self.hp -= amount

        if self.hp <= 0:
            self.hp = 0
            results.append({"dead": self.owner, "xp": self.xp})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []
        damage = self.power_level - target.fighter.defense_level

        if damage > 0:
            results.append(
                {
                    "message": Message(
                        f"{self.owner.name.capitalize()} attacks {target.name} for {damage} hit points.",
                        tcod.white,
                    )
                }
            )
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append(
                {
                    "message": Message(
                        f"{self.owner.name.capitalize()} attacks {target.name} but does no damage.",
                        tcod.white,
                    )
                }
            )

        return results
