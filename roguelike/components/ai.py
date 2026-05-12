from __future__ import annotations

from dataclasses import dataclass
from random import randint
from typing import Any, List, Dict, Optional

from tcod import libtcodpy

from roguelike.colors import Colors
from roguelike.game_messages import Message


# ---------------------------------------------------------------------------
# BASIC MONSTER AI
# ---------------------------------------------------------------------------

@dataclass
class BasicMonster:
    """
    Default monster behavior:
    - If player is visible: move toward or attack.
    - Otherwise: do nothing.
    """
    owner: Optional[Any] = None  # Entity that owns this AI

    def take_turn(self, target, fov_map, game_map, entities) -> List[Dict[str, Any]]:
        assert self.owner is not None
        results: List[Dict[str, Any]] = []
        monster = self.owner

        # Only act if visible to the player
        if libtcodpy.map_is_in_fov(fov_map, monster.x, monster.y):
            distance = monster.distance_to(target)

            if distance >= 2:
                monster.move_astar(target, entities, game_map)
            elif target.fighter.hp > 0:
                results.extend(monster.fighter.attack(target))

        return results


# ---------------------------------------------------------------------------
# CONFUSED MONSTER AI
# ---------------------------------------------------------------------------

@dataclass
class ConfusedMonster:
    """
    Temporary AI that causes random movement for a number of turns.
    Afterward, the previous AI is restored.
    """
    previous_ai: Any
    number_of_turns: int = 10
    owner: Optional[Any] = None  # Entity that owns this AI

    def take_turn(self, target, fov_map, game_map, entities) -> List[Dict[str, Any]]:
        assert self.owner is not None
        results: List[Dict[str, Any]] = []
        monster = self.owner

        if self.number_of_turns > 0:
            # Random step in any direction (including staying still)
            dx = randint(-1, 1)
            dy = randint(-1, 1)

            new_x = monster.x + dx
            new_y = monster.y + dy

            # Move only if the tile changes
            if dx != 0 or dy != 0:
                monster.move_towards(new_x, new_y, game_map, entities)

            self.number_of_turns -= 1
            return results

        # Confusion has ended — restore previous AI
        monster.ai = self.previous_ai
        monster.ai.owner = monster

        results.append({
            "message": Message(
                f"The {monster.name} is no longer confused!",
                Colors.red,
            )
        })

        return results
