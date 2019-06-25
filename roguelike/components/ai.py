from dataclasses import dataclass
from random import randint
from typing import Type

import tcod

from roguelike.game_messages import Message


@dataclass
class BasicMonster:
    def __post_init__(self):
        self.owner = self

    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner

        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results


@dataclass
class ConfusedMonster:
    previous_ai: Type[BasicMonster]
    number_of_turns: int = 10

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append(
                {
                    "message": Message(
                        f"The {self.owner.name} is no longer confused!", tcod.red
                    )
                }
            )

        return results
