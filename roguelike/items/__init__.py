from .antivenom import Antivenom
from .confusion_scroll import ConfusionScroll
from .fireball_scroll import FireballScroll
from .healing_potion import HealingPotion
from .lightning_scroll import LightningScroll
from .shield import Shield
from .sword import Sword

ITEM_WEIGHTS = [
    (HealingPotion, 50),
    (LightningScroll, 20),
    (FireballScroll, 15),
    (ConfusionScroll, 10),
    (Sword, 3),
    (Shield, 10),
    (Antivenom, 12),
]
