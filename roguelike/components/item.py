from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, List

from roguelike.game_messages import Message


@dataclass
class Item:
    """
    Represents an item that can be used, equipped, or consumed.
    Parameters such as `amount`, `damage`, `radius`, and `maximum_range`
    are passed directly to the item's use function.
    """
    use_function: Optional[Callable[..., List[Dict[str, Any]]]] = None
    targeting: bool = False
    targeting_message: Optional[Message] = None

    # Explicit parameters used by item functions
    amount: int | None = None
    damage: int | None = None
    radius: int | None = None
    maximum_range: int | None = None

    # Additional keyword arguments for item functions
    function_kwargs: Dict[str, Any] = field(default_factory=dict)

    # Entity that owns this item component
    owner: Optional[Any] = None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def is_consumable(self) -> bool:
        """Return True if this item has a use function."""
        return self.use_function is not None

    def requires_target(self) -> bool:
        """Return True if this item requires a target to use."""
        return self.targeting

    def __repr__(self) -> str:
        return f"Item(use_function={self.use_function}, owner={self.owner})"
