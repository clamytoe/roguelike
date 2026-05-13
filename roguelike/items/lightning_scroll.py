from roguelike.colors import Colors
from roguelike.item_functions import cast_lightning

from .base_item import BaseItem


class LightningScroll(BaseItem):
    char = "#"
    color = Colors.yellow
    name = "Lightning Scroll"
    use_function = cast_lightning
    function_kwargs = {"damage": 40, "maximum_range": 5}
