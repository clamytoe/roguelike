from __future__ import annotations

from typing import List, Dict, Any, Sequence
import random


# ---------------------------------------------------------------------------
# Dungeon scaling helper
# ---------------------------------------------------------------------------

def from_dungeon_level(
    table: List[Sequence[int]],
    dungeon_level: int
) -> int:
    """
    Given a table of (value, min_level), return the highest value
    whose min_level <= dungeon_level.
    """
    for value, level in reversed(table):
        if dungeon_level >= level:
            return value
    return 0


# ---------------------------------------------------------------------------
# Weighted random choice (index)
# ---------------------------------------------------------------------------

def random_choice_index(chances: List[int]) -> int:
    """
    Given a list of weights, return an index chosen according to those weights.
    """
    total = sum(chances)
    r = random.uniform(0, total)

    running = 0.0
    for i, weight in enumerate(chances):
        running += weight
        if r <= running:
            return i

    # Should never happen, but fallback to last index
    return len(chances) - 1


# ---------------------------------------------------------------------------
# Weighted random choice (dict)
# ---------------------------------------------------------------------------

def random_choice_from_dict(choice_dict: Dict[Any, int]) -> Any:
    """
    Given a dict of {item: weight}, return a randomly chosen item.
    """
    choices = list(choice_dict.keys())
    weights = list(choice_dict.values())
    index = random_choice_index(weights)
    return choices[index]
