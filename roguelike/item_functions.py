from __future__ import annotations

from typing import List, Dict, Any, Optional

import tcod

from roguelike.components.ai import ConfusedMonster
from .colors import Colors
from .game_messages import Message


# ---------------------------------------------------------------------------
# HEALING
# ---------------------------------------------------------------------------

def heal(*args, **kwargs) -> List[Dict[str, Any]]:
    entity = args[0]
    amount: int = kwargs.get("amount", 0)

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({
            "consumed": False,
            "message": Message("You are already at full health.", Colors.yellow),
        })
    else:
        entity.fighter.heal(amount)
        results.append({
            "consumed": True,
            "message": Message("Your wounds start to feel better!", Colors.green),
        })

    return results


# ---------------------------------------------------------------------------
# LIGHTNING
# ---------------------------------------------------------------------------

def cast_lightning(*args, **kwargs) -> List[Dict[str, Any]]:
    caster = args[0]
    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    damage = kwargs.get("damage")
    maximum_range = kwargs.get("maximum_range")

    results = []

    target = None
    max_range = maximum_range
    assert max_range is not None
    closest_distance = max_range + 1

    ents = entities
    assert ents is not None

    for entity in ents:
        if (
            entity.fighter
            and entity is not caster
            and tcod.map_is_in_fov(fov_map, entity.x, entity.y)
        ):
            distance = caster.distance_to(entity)
            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({
            "consumed": True,
            "target": target,
            "message": Message(
                f"A lightning bolt strikes the {target.name}! "
                f"It deals {damage} damage.",
                Colors.light_blue,
            ),
        })
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({
            "consumed": False,
            "target": None,
            "message": Message("No enemy is close enough to strike.", Colors.red),
        })

    return results


# ---------------------------------------------------------------------------
# FIREBALL
# ---------------------------------------------------------------------------

def cast_fireball(*args, **kwargs) -> List[Dict[str, Any]]:
    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    damage = kwargs.get("damage")
    radius = kwargs.get("radius")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    ents = entities
    assert ents is not None

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({
            "consumed": False,
            "message": Message(
                "You cannot target a tile outside your field of view.",
                Colors.yellow,
            ),
        })
        return results

    results.append({
        "consumed": True,
        "message": Message(
            f"The fireball explodes, burning everything within {radius} tiles!",
            Colors.orange,
        ),
    })

    for entity in ents:
        if entity.fighter and entity.distance(target_x, target_y) <= radius:
            results.append({
                "message": Message(
                    f"The {entity.name} is burned for {damage} HP.",
                    Colors.orange,
                )
            })
            results.extend(entity.fighter.take_damage(damage))

    return results


# ---------------------------------------------------------------------------
# CONFUSE
# ---------------------------------------------------------------------------

def cast_confuse(*args, **kwargs) -> List[Dict[str, Any]]:
    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    ents = entities
    assert ents is not None

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({
            "consumed": False,
            "message": Message(
                "You cannot target a tile outside your field of view.",
                Colors.yellow,
            ),
        })
        return results

    for entity in ents:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)
            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({
                "consumed": True,
                "message": Message(
                    f"The eyes of the {entity.name} glaze over as it becomes confused!",
                    Colors.light_green,
                ),
            })
            break
    else:
        results.append({
            "consumed": False,
            "message": Message(
                "There is no targetable enemy at that location.",
                Colors.yellow,
            ),
        })

    return results
