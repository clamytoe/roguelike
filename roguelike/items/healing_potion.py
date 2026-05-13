from roguelike.colors import Colors
from roguelike.item_functions import heal

from .base_item import BaseItem


class HealingPotion(BaseItem):
    char = "!"
    color = Colors.violet
    name = "Healing Potion"
    use_function = heal
    function_kwargs = {"amount": 40}
