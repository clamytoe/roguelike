from __future__ import annotations

# Import all monster classes so they are available at package level
from .giant_rat import GiantRat
from .vampire_bat import VampireBat
from .pit_viper import PitViper
from .zombie import Zombie
from .cave_scorpion import CaveScorpion
from .skeleton_archer import SkeletonArcher
from .cultist import Cultist
from .dire_bear import DireBear
from .floating_eye import FloatingEye
from .young_dragon import YoungDragon

# A simple, flat monster table (equal weight)
MONSTER_TABLE = [
    GiantRat,
    VampireBat,
    PitViper,
    Zombie,
    CaveScorpion,
    SkeletonArcher,
    Cultist,
    DireBear,
    FloatingEye,
    YoungDragon,
]

# Optional: weighted spawn table (recommended)
MONSTER_WEIGHTS = [
    (GiantRat, 30),
    (VampireBat, 20),
    (PitViper, 15),
    (Zombie, 15),
    (CaveScorpion, 12),
    (SkeletonArcher, 10),
    (Cultist, 8),
    (DireBear, 4),
    (FloatingEye, 6),
    (YoungDragon, 1),
]

# Optional: depth‑based spawn logic
def monsters_for_depth(depth: int):
    """Return a list of monsters appropriate for the given dungeon depth."""
    if depth <= 2:
        return [GiantRat, VampireBat, PitViper]
    elif depth <= 4:
        return [GiantRat, VampireBat, PitViper, Zombie, CaveScorpion]
    elif depth <= 6:
        return [Zombie, CaveScorpion, SkeletonArcher, Cultist]
    elif depth <= 8:
        return [SkeletonArcher, Cultist, DireBear, FloatingEye]
    else:
        return [DireBear, FloatingEye, YoungDragon]
