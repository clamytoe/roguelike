from dataclasses import dataclass

from roguelike.game_messages import Message


@dataclass
class Fighter:
    hp: int
    defense: int
    power: int

    def __post_init__(self):
        self.max_hp: int = self.hp

    def take_damage(self, amount):
        results = []
        self.hp -= amount

        if self.hp <= 0:
            self.hp = 0
            results.append({"dead": self.owner})

        return results

    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append(
                {
                    "message": Message(
                        f"{self.owner.name.capitalize()} attacks {target.name} for {str(damage)} hit points."
                    )
                }
            )
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append(
                {
                    "message": Message(
                        f"{self.owner.name.capitalize()} attacks {target.name} but does no damage."
                    )
                }
            )

        return results
