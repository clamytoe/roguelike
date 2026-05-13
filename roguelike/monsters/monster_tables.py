from .cave_spider import CaveSpider
from .pit_viper import PitViper
from .cave_scorpion import CaveScorpion
from .zombie import Zombie
from .skeleton_archer import SkeletonArcher
from .cultist import Cultist
from .dire_bear import DireBear
from .floating_eye import FloatingEye
from .young_dragon import YoungDragon
from .giant_rat import GiantRat
from .goblin import Goblin
from .orc import Orc
from .troll import Troll

# Depth-based monster spawn tables
MONSTER_TABLE = {
    1: [
        (GiantRat, 40),
        (Goblin, 30),
        (CaveSpider, 20),   # weak poison, okay for floor 1
        (Zombie, 10),
    ],

    2: [
        (GiantRat, 20),
        (Goblin, 20),
        (CaveSpider, 20),
        (PitViper, 20),     # introduce vipers here
        (Zombie, 20),
    ],

    3: [
        (Goblin, 15),
        (CaveSpider, 15),
        (PitViper, 25),
        (CaveScorpion, 20), # introduce scorpions here
        (Zombie, 25),
    ],

    4: [
        (Orc, 40),          # classic mid‑tier bruiser
        (Goblin, 20),
        (PitViper, 20),
        (CaveScorpion, 20),
    ],

    5: [
        (Orc, 30),
        (Troll, 20),        # introduce trolls here
        (SkeletonArcher, 20),
        (Cultist, 20),
        (CaveScorpion, 10),
    ],

    6: [
        (Orc, 20),
        (Troll, 25),
        (SkeletonArcher, 20),
        (Cultist, 20),
        (DireBear, 10),
        (FloatingEye, 5),
    ],

    7: [
        (Troll, 25),
        (SkeletonArcher, 20),
        (Cultist, 20),
        (DireBear, 20),
        (FloatingEye, 15),
    ],

    8: [
        (Troll, 20),
        (DireBear, 25),
        (FloatingEye, 25),
        (Cultist, 20),
        (SkeletonArcher, 10),
    ],

    9: [
        (DireBear, 30),
        (FloatingEye, 30),
        (Cultist, 20),
        (Troll, 20),
    ],

    10: [
        (DireBear, 20),
        (FloatingEye, 20),
        (Cultist, 20),
        (Troll, 20),
        (YoungDragon, 5),   # dragons start here
    ],
}




def get_monster_for_depth(rng, depth):
    # Clamp depth to max table
    depth = min(depth, max(MONSTER_TABLE.keys()))
    table = MONSTER_TABLE[depth]

    total = sum(weight for _, weight in table)
    roll = rng.randint(1, total)

    running = 0
    for monster_cls, weight in table:
        running += weight
        if roll <= running:
            return monster_cls

    return table[-1][0]  # fallback
