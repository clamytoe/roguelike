from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Dict, Optional

from roguelike.colors import Colors
from roguelike.game_messages import Message


@dataclass
class Fighter:
    """
    Handles combat stats, damage, healing, and attack logic.
    """
    hp: int
    defense: int
    power: int
    name: str = ""
    xp: int = 0

    base_max_hp: int = 0
    base_defense: int = 0
    base_power: int = 0

    owner: Optional[Any] = None  # Entity that owns this component

    def __post_init__(self):
        # Initialize base stats only once
        if self.base_max_hp == 0:
            self.base_max_hp = self.hp
        if self.base_defense == 0:
            self.base_defense = self.defense
        if self.base_power == 0:
            self.base_power = self.power

    # ----------------------------------------------------------------------
    # Derived stats
    # ----------------------------------------------------------------------
    @property
    def max_hp(self) -> int:
        bonus = self.owner.equipment.max_hp_bonus if self.owner and self.owner.equipment else 0
        return self.base_max_hp + bonus

    @property
    def power_level(self) -> int:
        bonus = self.owner.equipment.power_bonus if self.owner and self.owner.equipment else 0
        return self.base_power + bonus

    @property
    def defense_level(self) -> int:
        bonus = self.owner.equipment.defense_bonus if self.owner and self.owner.equipment else 0
        return self.base_defense + bonus

    # ----------------------------------------------------------------------
    # Combat
    # ----------------------------------------------------------------------
    def take_damage(self, amount: int) -> List[Dict[str, Any]]:
        """
        Apply damage and return results (death, XP, etc.).
        """
        results: List[Dict[str, Any]] = []
        self.hp -= amount

        if self.hp <= 0:
            self.hp = 0
            results.append({"dead": self.owner, "xp": self.xp})

        return results

    def heal(self, amount: int) -> None:
        """
        Heal the fighter, without exceeding max HP.
        """
        self.hp = min(self.hp + amount, self.max_hp)

    def attack(self, target) -> List[Dict[str, Any]]:
        """
        Perform an attack on the target and return combat results.
        """
        assert self.owner is not None
        results: List[Dict[str, Any]] = []
        damage = self.power_level - target.fighter.defense_level

        # Determine color based on attacker/defender roles
        if getattr(self.owner, "is_player", False):
            attack_color = Colors.light_green
        elif getattr(target, "is_player", False):
            attack_color = Colors.light_red
        else:
            attack_color = Colors.white

        if damage > 0:
            results.append({
                "message": Message(
                    f"{self.owner.name.capitalize()} attacks {target.name} for {damage} hit points.",
                    attack_color,
                )
            })
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({
                "message": Message(
                    f"{self.owner.name.capitalize()} attacks {target.name} but does no damage.",
                    attack_color,
                )
            })

        return results
