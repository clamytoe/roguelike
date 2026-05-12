from __future__ import annotations

from typing import Tuple, List, Dict, Any

from .colors import Colors
from .game_messages import Message
from .game_states import GameStates
from .render_functions import RenderOrder
from .entity import Entity


# ---------------------------------------------------------------------------
# Player death
# ---------------------------------------------------------------------------

def kill_player(player: Entity) -> Tuple[Message, GameStates]:
    """
    Handle player death and return the death message and new game state.
    """
    player.char = "%"
    player.color = Colors.dark_red

    death_message = Message("You died!", Colors.red)
    return death_message, GameStates.PLAYER_DEAD


# ---------------------------------------------------------------------------
# Monster death
# ---------------------------------------------------------------------------

def kill_monster(monster: Entity) -> Message:
    """
    Handle monster death, mutate the entity into a corpse, and return a message.
    """
    death_message = Message(
        f"{monster.name.capitalize()} is dead!",
        Colors.orange,
    )

    _transform_into_corpse(monster)
    return death_message


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _transform_into_corpse(entity: Entity) -> None:
    """
    Convert an entity into a non-blocking corpse.
    """
    entity.char = "%"
    entity.color = Colors.dark_red
    entity.blocks = False
    entity.fighter = None
    entity.ai = None
    entity.name = f"remains of {entity.name}"
    entity.render_order = RenderOrder.CORPSE
