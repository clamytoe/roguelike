from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

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

    poison_turns: int = 0
    poison_damage: int = 0

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
        bonus = (
            self.owner.equipment.max_hp_bonus
            if self.owner and self.owner.equipment
            else 0
        )
        return self.base_max_hp + bonus

    @property
    def power_level(self) -> int:
        bonus = (
            self.owner.equipment.power_bonus
            if self.owner and self.owner.equipment
            else 0
        )
        return self.base_power + bonus

    @property
    def defense_level(self) -> int:
        bonus = (
            self.owner.equipment.defense_bonus
            if self.owner and self.owner.equipment
            else 0
        )
        return self.base_defense + bonus

    # ----------------------------------------------------------------------
    # Combat
    # ----------------------------------------------------------------------
    def on_turn(self, owner):
        results = []

        if self.poison_turns > 0:
            self.poison_turns -= 1
            owner.fighter.take_damage(self.poison_damage)
            results.append({
                "message": Message(f"{owner.name} suffers poison damage!", Colors.violet)
            })

        return results

    def apply_poison(self, turns: int, damage: int):
        self.poison_turns = turns
        self.poison_damage = damage

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
            verb = "hit"
            msg = f"You {verb} the {target.name} for {damage} damage!"
        elif getattr(target, "is_player", False):
            attack_color = Colors.light_red
            verb = "hits"
            msg = f"The {self.owner.name} {verb} you for {damage} damage!"
        else:
            attack_color = Colors.white
            verb = "hits"
            msg = f"{self.owner.name} {verb} {target.name} for {damage} damage."

        if damage > 0:
            results.append({"message": Message(msg, attack_color)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({
                "message": Message(
                    f"{self.owner.name} attacks {target.name} but does no damage.",
                    attack_color,
                )
            })

        return results

