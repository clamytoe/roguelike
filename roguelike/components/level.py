from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Level:
    """
    Tracks XP, level progression, and level-up thresholds.
    """
    current_level: int = 1
    current_xp: int = 0
    level_up_base: int = 200
    level_up_factor: int = 150

    owner: Optional[Any] = None  # Entity that owns this component

    # ------------------------------------------------------------------
    # XP thresholds
    # ------------------------------------------------------------------
    @property
    def experience_to_next_level(self) -> int:
        """
        XP required to reach the next level.
        """
        return self.level_up_base + self.current_level * self.level_up_factor

    # ------------------------------------------------------------------
    # XP gain
    # ------------------------------------------------------------------
    def add_xp(self, xp: int) -> bool:
        """
        Add XP and return True if one or more level-ups occurred.
        """
        self.current_xp += xp
        leveled_up = False

        # Support multiple level-ups from a single XP gain
        while self.current_xp >= self.experience_to_next_level:
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1
            leveled_up = True

        return leveled_up
